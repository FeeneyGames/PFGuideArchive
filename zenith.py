from bs4 import BeautifulSoup


ZENITH_BACKUP_PATH = r"ZenithGames\Zenith Games The Comprehensive Pathfinder Guides Guide.html"
ZENITH_DIV_ID = "post-body-500675332292381825"


class ZenithParser():
    """Parse "The Comprehensive Pathfinder Guides Guide" by Zenith Games
    """
    def __init__(self):
        with open(ZENITH_BACKUP_PATH) as f:
            soup = BeautifulSoup(f, "html.parser")
        self.post_div = soup.find(id=ZENITH_DIV_ID)

    def get_docs_urls(self):
        """Get Google Docs URLs linked in the HTML

        Returns:
            (list, list): List of Google Docs URLs
                          List of labels given to the links
        """
        docs_urls = []
        link_labels = []
        for tag in self.post_div.find_all("a"):
            url = tag["href"]
            if url.startswith("https://docs.google.com") or \
               url.startswith("https://drive.google.com"):
                docs_urls += [url]
                link_labels += [tag.text]
        return docs_urls, link_labels

    def get_guide_urls(self):
        """Get URLs to guides linked in the HTML

        Returns:
            (list, list, list): List of Google Docs URLs
                                List of labels given to the links
                                List of classes for the links
        """
        # data structures for returns
        urls = []
        link_labels = []
        link_class = []
        # data structures for tracking classes for links
        cur_class = None
        dict_counter = {}
        for tag in self.post_div.find_all("a"):
            url = tag["href"]
            # update class for the links if boundary found
            if url in url_to_class:
                dict_count = min(dict_counter.get(url, 0), len(url_to_class[url]) - 1)
                cur_class = url_to_class[url][dict_count]
                dict_counter[url] = dict_counter.get(url, 0) + 1
            # record the data for the link
            if cur_class is not None:
                urls += [url]
                link_labels += [tag.text]
                link_class += [cur_class]
        return urls, link_labels, link_class

    def print_class_dict_rough(self):
        """Prints a rough version of class_to_url for updating
        """
        for tag in self.post_div.find_all("b"):
            if tag.next_sibling is not None and tag.next_sibling.name == "br":
                text = str(tag.text).lower()
                while " " in text:
                    text = text.replace(" ", "-")
                i = 0
                while i < len(text):
                    if not text[i].isalpha() and text[i] != "-":
                        text = text[:i] + text[i + 1:]
                    else:
                        i += 1
                if len(text) > 0:
                    if tag.find_next("a") is not None:
                        link = tag.find_next("a")["href"]
                    else:
                        link = ""
                    print("\"" + text + "\":\"" + link + "\",")


class_to_url = {
    "alchemist": "http://zenithgames.blogspot.com/2015/11/zeniths-guide-to-alchemist-part-i.html",
    "arcanist": "https://docs.google.com/document/d/19eADtzhxjNq8n8esfos6gnmotwPAIFot-ouLztuQtqA/pub",  # noqa: E501
    "antipaladin": "https://drive.google.com/file/d/0B9vv1a7v3y5BZjJSaU5wY3NvdEk/view",
    "barbarian": "http://www.giantitp.com/forums/showthread.php?p=12732426#post12732426",
    "bard": "https://docs.google.com/document/d/1ogz8HL6GeguT-tN3-6HxXiF_G7mg_tyAQ59V9kPg6g4/edit?pli=1",  # noqa: E501
    "bloodrager": "https://docs.google.com/document/d/1uV52XseHRUMKOM-fLF6oXwkF-bcmmPk93XR8u02-sYw/edit",  # noqa: E501
    "brawler": "http://paizo.com/threads/rzs2rn5i?Happy-Feet-Wombo-Combo-A-guide-to-getting",
    "cavalier": "https://docs.google.com/document/d/1uuAB8SfE5ssZLYwa1LuQQ4haz1tD1q28Iyl8XAdMNxY/edit?hl=en_US",  # noqa: E501
    "cleric": "https://docs.google.com/document/d/1h6-_4HvPvV-Tt7I67Gi_oPhgHmeDVA5SBl-WrJSgf5s/edit?hl=en#",  # noqa: E501
    "druid": "https://docs.google.com/document/pub?id=1Y_uvQ0fgmLR9aW-OoAD_rbI-3iMJVQmxifLpA1s5EXg",
    "fighter": "https://docs.google.com/document/d/178CAoRPv-ST4ntUWwDFmkX5mi5Tm3pB1MGtoLXpG1D4/edit",  # noqa: E501
    "gunslinger": "http://paizo.com/threads/rzs2modi?DrakeRockets-Guide-to-Grand-Gunslinginger#1",
    "hunter": "http://paizo.com/threads/rzs2u0vl?Working-on-a-guide-to-the-HUNTER-base-class",
    "inquisitor": "https://drive.google.com/file/d/0B9vv1a7v3y5BLTlQVlZ6TDI0RTg/view",
    "investigator": "https://www.reddit.com/r/Pathfinder_RPG/comments/he18bp/the_investigators_academy_a_new_guide_to_the/",  # noqa: E501
    "kineticist": "http://paizo.com/threads/rzs2su6f?Mastering-the-Elements-N-Jollys-guide-to-the",
    "magus": "https://docs.google.com/document/d/1fSJuL1O4hs15NMk-y4MXbH9D_qt9V7iwhY2y9HDrs74/edit",
    "medium": "http://www.giantitp.com/forums/showthread.php?454839-CTP-s-Medium-Guide",
    "mesmerist": "https://docs.google.com/document/d/1vGa7fsHbvWNTgPlKlEBJfRYE_vHNKt7dpJHUwiAv4f0/edit",  # noqa: E501
    "monk": "http://paizo.com/threads/rzs2nix8?Zen-and-the-Art-of-Monk-Maintenance-A-Guide#1",
    "monk-unchained": "https://docs.google.com/document/d/1vtxGT6RArwUBqSMTco-ekm9azMXWGox9tTD6Wp3rYTE/edit",  # noqa: E501
    "ninja": "http://zenithgames.blogspot.com/2014/08/zeniths-guide-to-ninja-part-i.html",
    "occultist": "http://www.thedicedecide.com/mack-blog/of-wands-cups-and-blades-a-guide-to-the-pathfinder-occultist/",  # noqa: E501
    "oracle": "https://docs.google.com/document/d/1WdtrZCESRmVfljXY196wMrMLTnS8Uzk4DEk3oQdVZok/edit?hl=en_US",  # noqa: E501
    "paladin": "https://drive.google.com/file/d/0B9vv1a7v3y5BZjJSaU5wY3NvdEk/view",
    "psychic": "https://docs.google.com/document/d/1JRq3ywFhF3BsJH1tTj5JgRhN2gvwiyUaLUgvDYv-gCI/edit?copiedFromTrash",  # noqa: E501
    "ranger": "https://docs.google.com/document/d/1JRq3ywFhF3BsJH1tTj5JgRhN2gvwiyUaLUgvDYv-gCI/edit?copiedFromTrash",  # noqa: E501
    "rogue": "http://paizo.com/threads/rzs2qw2l?Moxie-A-Practical-Guide-to-Roguing-with-Style",
    "rogue-unchained": "https://docs.google.com/document/d/1zLDFgiwZt_vPVlOcgR7QDAvskcH34uG1FuKPXTnpuEg/view",  # noqa: E501
    "samurai": "https://docs.google.com/document/d/1gD4kwJXJPMUDGuKsvYiL03ACj-ZqiwDcMrkHtV9mmKI/edit",  # noqa: E501
    "shaman": "http://paizo.com/threads/rzs2rlmn?The-Seers-Catalog",
    "shifter": "http://paizo.com/threads/rzs2uuj6?Archmage-Variels-Guide-to-the-Shifter",
    "skald": "http://paizo.com/threads/rzs2rloh?Pseudoguide-to-the-Skald-or-How-to-be-Metal",
    "slayer": "http://paizo.com/threads/rzs2s91q?A-Study-of-Slayers-A-Class-Guide",
    "sorcerer": "http://zenithgames.blogspot.com/2017/11/inner-power-guide-to-sorcerer.html",
    "spiritualist": "http://www.giantitp.com/forums/showthread.php?t=184592",
    "summoner": "http://www.giantitp.com/forums/showthread.php?t=184592",
    "summoner-unchained": "http://paizo.com/threads/rzs2s8ur?Unchained-Summoner-Guide#1",
    "swashbuckler": "http://paizo.com/threads/rzs2rk3q?A-Guide-To-The-Swashbuckler",
    "vampire-hunter": "http://paizo.com/threads/rzs2tn7y?I-Am-Vengeance-I-am-the-Night-FedoraFerrets",  # noqa: E501
    "vigilante": "http://paizo.com/threads/rzs2tn7y?I-Am-Vengeance-I-am-the-Night-FedoraFerrets",
    "warpriest": "http://paizo.com/threads/rzs2tbb4?Piercing-the-Heavens-N-Jollys-guide-to-the#1",
    "witch": "https://docs.google.com/document/d/1YkARuboGbaCVdOpcgoA0epQFqBlCygzzUsgaBdba9BE/edit",
    "wizard": "https://docs.google.com/document/d/1mmafMuRRd3ubCMhCNmOomLUn_YvaVXiHwSyuC1YDrNc/edit",  # noqa: E501
    "arcane-archer": "http://zenithgames.blogspot.com/2015/03/the-human-diversions-guide-to-caster.html",  # noqa: E501
    "arcane-trickster": "https://docs.google.com/document/d/1QnrGZYKGA0QXaob_iVo2rGtG1cC7HvRRa7cGYV_mBnE/edit",  # noqa: E501
    "arclord-of-nex": "https://drive.google.com/file/d/0B_E5ym1-3f-uRUItWXUzQzZnQjg/view",
    "assassin": "https://docs.google.com/document/d/1VfVbEOKnZrQ3P4V_WC6RNn4hQGjOWbIxc0aXIrHergM/edit?pli=1",  # noqa: E501
    "battle-herald": "https://docs.google.com/document/d/1BbS5z7Ls4D7IejlbIONq0NJyQtPK1wWJU2olTXwlRUA/pub",  # noqa: E501
    "champion-of-irori": "https://docs.google.com/file/d/0B1bu5RkMqNkZbHpHRF9RX09ZWE0/edit?usp=sharing",  # noqa: E501
    "demoniac": "https://docs.google.com/document/d/1TyBG3PNwtZ2OmNaUo8QGggEWxzrD0Odm6OsDgsXUglA/edit",  # noqa: E501
    "diabolist": "https://drive.google.com/file/d/0B0NP0qPr6hs-czVmdXBXX3BrOHM/view",
    "dragon-disciple": "https://docs.google.com/document/d/1cmswe4jHDb1Vcm3oQME3mxUelX_WzKbQ8r9_1mwQS6M/edit?hl=en_US&pli=1",  # noqa: E501
    "duelist": "https://docs.google.com/document/d/1xRicfKx_3l0G6C84gn8O3PjeMnMq3QnMsJ5_eJxCccM/edit?pli=1",  # noqa: E501
    "eldritch-knight": "https://docs.google.com/document/d/10jQgMH85x_YuhgtOYMiEI7b3WyM08MXDbt-fNPRuZ6Y/edit",  # noqa: E501
    "hellknight": "https://docs.google.com/document/d/1UY7y8rSIQ3bEmuNmzAh7Ur5GaW-TVqBTp3usC1IcPu8/edit",  # noqa: E501
    "mystery-cultist": "https://docs.google.com/document/d/1ySlbpe9AmxYpnuTc3rtYODhs-2HTbp6Ky5_xoaG7QJ8/edit",  # noqa: E501
    "mystic-theurge": "https://docs.google.com/document/d/1NPs0YHuWnoQu9yao-Jk0lQAyZy7FyyWMcoyoXKo0Sn8/edit",  # noqa: E501
    "pathfinder-chronicler": "https://docs.google.com/document/d/1fqG6GMiyfn9dfVMpZN1hdIovZ46FLE2ofGqS_RqSQ7Q/edit?pli=1",  # noqa: E501
    "stalwart-defender": "https://docs.google.com/document/d/1mR2SAPeQg6HYo6nnMkd1GEA4CPXpJhZWe5bxsDU9wpQ/edit#",  # noqa: E501
    "rage-prophet": "https://docs.google.com/document/d/1FJiX9cFcJ3tCJmlIBpzgL9bSMcSVLHgwDfTXokJedJU/edit#heading=h.97g3zpcb0bqy",  # noqa: E501
    "shadow-dancer": "https://docs.google.com/document/d/1ECKpD15DbcDuEyPKiR1BsY2JLSGRjLwEp8Fncq3Smjw/edit",  # noqa: E501
    "aegis": "https://docs.google.com/document/d/1U7FY9aFIXveyvQyUV2W7X2yZsLZlOpQARrWkC4DNmC0/edit?usp=sharing",  # noqa: E501
    "conscript": "https://img.4plebs.org/boards/tg/image/1511/40/1511406264160.pdf",
    "cryptic": "https://docs.google.com/document/d/1RxC-BKcPvvsQELUGZVCCrd7Z5Rp5K3LoB_RGdjaQ1TA/edit?usp=sharing",  # noqa: E501
    "daevic": "https://docs.google.com/document/d/1klD7v0-tfZeKm3oOyD12jOxPTBKv5_9Tc9Y6QIPAz6I/edit",  # noqa: E501
    "draconic-exemplar": "http://www.giantitp.com/forums/showthread.php?473271-So-you-want-to-be-a-dragon-A-real-one-Sure-I-ll-help!-%28Guide-to-Draconic-Exemplar%29",  # noqa: E501
    "dread": "https://docs.google.com/document/d/1asiWRZfTDtHd6TVkdprc85wkggrmu8FDmzEyjNUrBMU/edit",
    "elementalist": "https://docs.google.com/document/d/15a4d5ga61bcWMuqJxBOEleKPSsSUgkzz-Yj7POJNhD8/edit",  # noqa: E501
    "guru": "https://docs.google.com/document/d/1oSSJqPPNSfOQvNM0H2p9Aqeu2kejSRoujzJzU0gwOdM/edit",
    "harbinger": "https://docs.google.com/document/d/1kSmuTy1Hmg6w0lYSW7xoyJKRdAOgTDU1piejfEt37Yg/edit",  # noqa: E501
    "marksman": "https://docs.google.com/document/d/1h_LDT7hg3El9JGxWQjA-1CvMunpbOjrfW8RJglFq9ys/edit",  # noqa: E501
    "mystic": "https://docs.google.com/document/d/1sCIm2NOaSgY5hM1fFaBqlMaCerLeyBq0UPonK9fTiY8/edit",  # noqa: E501
    "nightblade": "http://www.giantitp.com/forums/showthread.php?418529-Into-the-Darkness-a-Guide-to-the-Nightblade",  # noqa: E501
    "pactmaker": "https://docs.google.com/document/d/1FGgq3CJYQaeAugHvaaws-ak1ryZzijKou_w1KN0D9HA/pub",  # noqa: E501
    "psion": "https://docs.google.com/document/d/1YVapC-VhuKDQ5vx4T2go8v4HdY6vX7U_FUA-IEn_yrM/edit#",  # noqa: E501
    "psychic-warrior": "https://docs.google.com/document/d/1kM0wGV_JnkCU6cYAdLFP-vzlPvU4PNDLR3rDMQBX-9Y/edit",  # noqa: E501
    "sentinel": "https://img.fireden.net/tg/image/1516/50/1516504855329.pdf",
    "soulknife": "http://www.giantitp.com/forums/showthread.php?t=203014",
    "stalker": "http://www.giantitp.com/forums/showthread.php?317986-PF-Striking-from-the-Shadows-a-Guide-to-the-PoW-Stalker",  # noqa: E501
    "tactician": "http://www.giantitp.com/forums/showthread.php?t=228324",
    "thaumaturge": "https://docs.google.com/document/d/1stQNHUqRPpEIjMCvyx9CNhxBYEESUHXDRTj933RPqiM/edit#heading=h.30j0zll",  # noqa: E501
    "vitalist": "http://www.giantitp.com/forums/showthread.php?t=222365",
    "vizier": "https://docs.google.com/document/d/1s_nhfamh0Uaqxmqe7u7in61OWT3lhAhVDEC9WQZ6jcc/edit",  # noqa: E501
    "warder": "http://www.giantitp.com/forums/showthread.php?348363-Defending-the-Weak-A-Guide-to-the-PoW-Warder-WIP",  # noqa: E501
    "warlord": "http://www.giantitp.com/forums/showthread.php?334608-PF-Leading-the-Battle-A-Guide-to-the-PoW-Warlord",  # noqa: E501
    "wilder": "https://docs.google.com/document/d/1bb4KrtEGyJ0mWkPdMC7_wXiSrZOUibk4GL32aidD1WM/edit",  # noqa: E501
    "zealot": "https://docs.google.com/document/d/1p3Bga5DyWoLW054p55E7V0rBLZbshPpEHzTjLFFYUqI/edit",  # noqa: E501
    "builds": "http://zenithgames.blogspot.com/2013/01/guide-to-builds.html",
    "race-guides": "http://zenithgames.blogspot.com/2015/06/races-of-pathfinder-optimization-guide.html",  # noqa: E501
    "equipment": "http://zenithgames.blogspot.com/2013/11/improving-your-class-with-items.html",
    "general-character-building": "https://docs.google.com/document/d/1UY1RrLleESzHZv2L6rkJnWihtzyazz1kvUzisZTO9TU/edit",  # noqa: E501
    "traits": "https://docs.google.com/document/d/1jAcuQltZd3DEhlUsgtvgbO21JxrUScqtmyp2lyWyOnI/edit?pli=1",  # noqa: E501
    "specific-strategies-tactics": "https://docs.google.com/document/d/1GG-j2Uu9bT3rGEMtS5tx8Fu_7i8heNyKxZDPBFwjN9E/edit",  # noqa: E501
    "variant-multi-classing": "https://docs.google.com/document/d/1AfAS7-neWhv8Gn1UDQ5hdISJisS_ij-AXrYUEsB6fPM/edit",  # noqa: E501
    "tips-tricks": "http://www.geekindustrialcomplex.com/articles/action-economy-time-savers",
    "summoned-monsters-and-animal-companions": "https://drive.google.com/file/d/1m6CtL-0cImywzv9ugTq85cL_j6U7ve4_/view",  # noqa: E501
    "specific-class-abilities": "https://docs.google.com/document/d/1JZKw8dVJxfnEy9rr5-oxZYc8yG02moIpxeSwktsp0JA/edit?pli=1",  # noqa: E501
    "spheres-of-might": "https://docs.google.com/document/d/1AiBjDGgWVjL_H72dJVRhy-OunseTzBAiHiU8MKIjO-M/edit",  # noqa: E501
    "gm-guides": "http://zenithgames.blogspot.com/2013/11/7-tips-for-new-gms.html",
    "mythic": "https://docs.google.com/document/d/1fD5YATlBMj5MuPOSDYlnLpnOQJZzn43bBE8LT6860B8/edit",  # noqa: E501
    "play-by-post": "http://paizo.com/threads/rzs2nr91?DHs-Guide-to-Play-By-Post-gaming",
    "pathfinder-society": "https://docs.google.com/document/d/1n7D4Y_W6jzhVYi2UzJqRArsyb7k6Y_i4Jm_uojDuiII/edit#",  # noqa: E501
    "guides-on-types-of-builds": "https://docs.google.com/document/d/1Kj_ppmS2m5Z4MNaSzW48rH9wTE72HihX_7s52u5gsbs/edit?hl=en_US&pli=1",    # noqa: E501
    "general": "https://docs.google.com/document/d/1ppOgELS9vstpTDwo9SeuqMKbfZ4kheetHZuKMp970Mo/edit",  # noqa: E501
    "other": "http://sojourngames.wordpress.com/2012/11/27/how-to-use-leadership-part-1-understanding-the-feat/",  # noqa: E501
}

url_to_class = {}
for key, val in class_to_url.items():
    url_to_class[val] = url_to_class.get(val, []) + [key]
