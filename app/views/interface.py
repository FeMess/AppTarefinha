import flet as ft
from app.models.database import ManagementSystemDatabase

sgbd = ManagementSystemDatabase()

class GUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = 'AppTarefinha'
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window.resizable = False
        self.page.window.width = 720
        self.page.window.height = 500
        self.page.window.always_on_top = True

    def get_tasks(self, status = None, tasks = []):
        self.task_gallery.controls.clear()
        tasks = sgbd.get_task()

        for task in tasks:
            task_control = ft.ListTile(
                leading= ft.Checkbox(
                    value= False if task[2] == 'Pendente' else True,
                    on_change= self.on_update_click,
                    data= {
                        'ID': task[0],
                        'Name': task[1],
                        'Status' : task[2]
                    }
                ),
                title= ft.Text(f'{task[1]}'),
                subtitle= ft.Text(f'{task[2]}'),
                bgcolor= ft.Colors.BLUE_50 if task[2] == "Completo" else ft.Colors.WHITE,
                trailing= ft.PopupMenuButton(
                    items=[
                        # ft.PopupMenuItem(
                        #     text= 'Editar',
                        #     icon= ft.Icons.EDIT,
                        #     on_click= ..., 
                        #     data= task[0]
                        # ),
                        ft.PopupMenuItem(
                            text= 'Excluir',
                            icon= ft.Icons.DELETE,
                            on_click= self.on_delete_click,
                            data= task[0]
                        )
                    ],
                    tooltip= 'Mais Opções'
                ) 
            )
            self.task_gallery.controls.append(task_control)
        self.task_gallery.update()

    def page_linkedin_launch(self, e):
        e.page.launch_url("https://www.linkedin.com/in/felipemesquita19/")

    def on_add_click(self, e):
        TaskName = self.input_task.value
        TaskName = TaskName.strip()
        if TaskName != "":
            sgbd.create_task(TaskName)
            self.input_task.value = ''
            self.input_task.update()
            self.get_tasks()

    def on_delete_click(self, e):
        task_ID = e.control.data
        sgbd.remove_task(task_ID)
        self.get_tasks()

    def on_update_click(self, e):
        all_task_data = e.control.data
        task_ID = all_task_data['ID']
        task_name = all_task_data['Name']
        task_status = 'Completo' if e.control.value == True else 'Pendente'
        sgbd.update_task(task_ID, task_name, task_status)
        self.get_tasks()

    def initialize(self):

        #Basic inputs & important controls
        self.input_task = ft.TextField(hint_text='Qual é a tarefa?', expand= True, on_submit= self.on_add_click)
        self.task_gallery = ft.Column(expand= True, scroll= ft.ScrollMode.ALWAYS)

        #GUI
        appBar = ft.AppBar(
            title= ft.Text('AppTarefinha', weight= ft.FontWeight.W_500, color= ft.Colors.BLACK),
            center_title= False,
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            icon= ft.Icons.LINK,
                            text= 'LinkedIn',
                            on_click= self.page_linkedin_launch
                        )
                    ]
                )
            ]
        )

        layout = ft.Row(
            height= self.page.window.height,
            expand=True,
            controls=[
                ft.NavigationRail(
                    selected_index= 0,
                    label_type= ft.NavigationRailLabelType.ALL,
                    # leading= ft.IconButton(ft.Icons.TASK, icon_size= 35, tooltip= 'AppTarefinha'),
                    destinations=[
                        ft.NavigationRailDestination(
                            icon= ft.Icons.BOOKMARK_BORDER_SHARP,
                            selected_icon= ft.Icons.BOOKMARK_SHARP,
                            label= 'Todos'
                        ),
                        ft.NavigationRailDestination(
                            icon= ft.Icons.BOOKMARK_REMOVE_OUTLINED,
                            selected_icon= ft.Icons.BOOKMARK_REMOVE_SHARP,
                            label= 'Pendente'
                        ),
                        ft.NavigationRailDestination(
                            icon= ft.Icons.BOOKMARK_ADDED_OUTLINED,
                            selected_icon= ft.Icons.BOOKMARK_ADDED_SHARP,
                            label= 'Completo'
                        )
                    ]
                ),
                ft.VerticalDivider(width=1),
                ft.Column(
                    expand= True,
                    controls=[
                        ft.Row(
                            alignment= ft.MainAxisAlignment.START,
                            controls=[
                                self.input_task,
                                ft.FloatingActionButton(
                                    icon= ft.Icons.ADD, 
                                    tooltip= 'Adicionar', 
                                    height= 50,
                                    on_click= self.on_add_click
                                ),
                            ]
                        ),
                        self.task_gallery
                    ]
                )
            ]
        )
    
        self.page.add(
            appBar,
            layout
        )

        self.get_tasks()