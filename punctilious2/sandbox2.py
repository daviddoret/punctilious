import rich
import rich.console
import rich.markdown
import rich.table


# prnt(grid)
# console = rich.console.Console()
s = '**hello**'
md = rich.markdown.Markdown(s)
console = rich.console.Console()
rich.print(md)
console.print(md)
