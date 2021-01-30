from pywebcopy import save_webpage


save_webpage("https://docs.google.com/document/d/1jkc2rDCkW5pVGB2px89SAHcKzAuDi79_dVuIQ2xxf9Q/pub",
             "archive",
             project_name="websites",
             reset_config=True,
             bypass_robots=True)
