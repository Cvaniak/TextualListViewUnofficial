from __future__ import annotations

from textual.layouts.vertical import VerticalLayout
from textual.layouts.grid import GridLayout
from textual.reactive import Reactive
from textual.widgets import Placeholder
from textual.widgets import ScrollView
from textual.widget import Widget
from textual.views import WindowView
from textual.events import Message
from textual.app import App
from textual import events


class _WindowViewMultipleWidgets(WindowView):
    layout: Reactive[VerticalLayout]
    def __init__(self, widgets, *args, **kwargs) -> None:
        super().__init__(widget = widgets[0], *args, **kwargs)
        for i in widgets[1:]:
            self.layout.add(i)

    async def remove_by_index(self, index=0):
        widgets = self.layout._widgets[:]
        self.layout.clear()
        for i, w in enumerate(widgets):
            if i != index:
                self.layout.add(w)

    async def remove_widget(self, widget):
        widgets = self.layout._widgets[:]
        self.layout.clear()
        for w in widgets:
            if w is not widget:
                self.layout.add(w)


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

    def refresh_all(self):
        self.window.layout.require_update()
        self.layout.require_update()
        self.window.refresh()
        self.vscroll.refresh()
        self.hscroll.refresh()

    async def add_widget(self, widget):
        self.window.layout.add(widget)
        self.refresh_all()

    async def remove_widget_by_index(self, index=0):
        await self.window.remove_by_index(index)
        self.refresh_all()

    async def remove_widget(self, widget):
        await self.window.remove_widget(widget)
        self.refresh_all()
    

if __name__ == "__main__":
    from textual.widgets import Footer

    class DeleteStatus(Message):
        def __init__(self, sender: Widget):
            super().__init__(sender)


    class DeletablePlaceholder(Placeholder):
        async def on_click(self, event: events.Click) -> None:
            await self.emit(DeleteStatus(self))


    class TestListView(App):
        async def action_add(self) -> None:
            await self.list_view.add_widget(DeletablePlaceholder(height=10))
            self.refresh()

        async def action_remove(self) -> None:
            await self.list_view.remove_widget_by_index()
            self.refresh()

        async def on_load(self, _: events.Load) -> None:
            await self.bind("a", "add()", "Add Widget")
            await self.bind("r", "remove()", "Remove Widget")
            await self.bind("Click Widget", "_()", "To delete it")

        async def on_mount(self, event: events.Mount) -> None:
            self.list_view = ListViewUo(widgets=[DeletablePlaceholder(height=10) for _ in range(7)])
            await self.view.dock(Footer(), edge="bottom")
            await self.view.dock(self.list_view)

        async def handle_delete_status(self, message: DeleteStatus):
            await self.list_view.remove_widget(message.sender)

    TestListView.run()
