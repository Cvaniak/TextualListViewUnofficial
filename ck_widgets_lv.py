from __future__ import annotations

from textual.layouts.grid import GridLayout
from textual.widgets import Placeholder
from textual.widgets import ScrollView
from textual.views import WindowView
from textual.app import App
from textual import events


class _WindowViewMultipleWidgets(WindowView):
    def __init__(self, widgets, *args, **kwargs) -> None:
        super().__init__(widget = widgets[0], *args, **kwargs)
        for i in widgets[1:]:
            self.layout.add(i)


class ListViewUo(ScrollView):
    def __init__(self, widgets, *args, **kwargs) -> None:
        super().__init__(widgets[0], *args, **kwargs)
        self.widgets_list = widgets

    async def on_mount(self, _: events.Mount) -> None:
        assert isinstance(self.layout, GridLayout)
        self.layout.place(
            vscroll=self.vscroll,
            hscroll=self.hscroll,
        )

        # Replace default self.window
        self.window = _WindowViewMultipleWidgets(widgets=self.widgets_list)
        self.layout.place(content=self.window)

        await self.layout.mount_all(self)


class TestListView(App):
    async def on_mount(self, event: events.Mount) -> None:
        await self.view.dock(ListViewUo(widgets=[Placeholder(height=10) for _ in range(20)]))


if __name__ == "__main__":
    TestListView.run()
