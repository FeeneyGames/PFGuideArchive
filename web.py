from functools import partial
from multiprocessing.dummy import Pool

from pywebcopy import webpage, config


# modified version of pywebcopy api's savewebpage to return filepath
def save_webpage_with_path(url, project_folder, html=None, project_name=None,
                           encoding=None, reset_config=False, popup=False, **kwargs):
    # Set up the global configuration
    config.setup_config(url, project_folder, project_name, **kwargs)

    # Create a object of web page
    wp = webpage()
    wp.url = config['project_url']
    wp.path = config['project_folder']

    #: Remove the extra files downloading if requested
    if not config.get('load_css'):
        wp.deregister_tag_handler('link')
        wp.deregister_tag_handler('style')
    if not config.get('load_javascript'):
        wp.deregister_tag_handler('script')
    if not config.get('load_images'):
        wp.deregister_tag_handler('img')

    if html:
        #: only set url in manual mode because its internally
        #: set in the get() method
        wp.set_source(html, encoding)

    else:
        wp.get(wp.url)

    # If encoding is specified then change it otherwise a default encoding is
    # always internally set by the get() method
    if encoding:
        wp.encoding = encoding

    # Instruct it to save the complete page
    wp.save_complete()

    if reset_config:
        # reset the config so that it does not mess up any con-current calls to
        # the different web pages
        config.reset_config()

    return wp.utx.file_path


def save_webpages_with_path(urls):
    num_threads = 4
    # save webpages on multiple threads
    thread_pool = Pool(num_threads)
    archive_url = partial(save_webpage_with_path,
        project_folder="archive",
        project_name="websites",
        reset_config=True,
        bypass_robots=True
    )
    archive_paths = thread_pool.map(archive_url, urls)
    # close threads, but don't bother waiting for them to free resources
    thread_pool.close()
    return archive_paths
