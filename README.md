# Unofficial [Textual](https://github.com/Textualize) List View (Scrollable list of widgets)
While waiting for [ticket](https://github.com/Textualize/textual/projects/1#card-66941810) (also mentioned [here](https://github.com/Textualize/textual/discussions/196)) and official `ListView`, you can use this dirty version that allows you to scroll thrue list of widgets.  

## Installation
This is not pip package but you can install this with pip:
```bash
pip3 install git+https://github.com/Cvaniak/TextualListViewUnofficial.git 
```

## Usage
Then in code you can use it this way:
```python3
from ck_widgets_lv import ListViewUo

class TestListView(App):
    async def on_mount(self, event: events.Mount) -> None:
        await self.view.dock(ListViewUo(widgets=[Placeholder(height=10) for _ in range(20)]))

if __name__ == "__main__":
    TestListView.run()
```


