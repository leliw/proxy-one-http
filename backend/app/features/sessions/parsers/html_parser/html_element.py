import bs4

from ampf.base.base_decorator import BaseDecorator


class HtmlElement(BaseDecorator[bs4.BeautifulSoup]):
    """Rozszerza PageElement z BeautifulSoup."""

    def __init__(self, body: str | bs4.PageElement) -> None:
        if isinstance(body, str):
            decorated = bs4.BeautifulSoup(body, "html.parser")
        else:
            decorated = body
        super().__init__(decorated)

    def prettify(self) -> str:
        ret = self.decorated.prettify()
        return ret.replace("\r", "")

    def info(self, parent: bs4.PageElement = None, ident: int = 0, max_ident: int = 5):
        """Pokazuje skróconą informację o zawartości elementu"""
        if not parent:
            print("=== childs ===")
            parent = self.decorated
        for child in parent.children:
            if child.name is not None:
                desc = ("  " * ident) + child.name
                if child.get("id") is not None:
                    desc += " id=" + child.get("id")
                print(desc)

                if ident < max_ident:
                    self.info(child, ident=ident + 1, max_ident=max_ident)
            else:
                # print(child)
                # print(('  ' * ident) +"<anonymous>")
                pass
