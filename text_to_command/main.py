import json

from text_to_command.entities import Application, Function, AppsConfiguration, SystemConfiguration


def apps_config_factory():
    return AppsConfiguration([
        Application(
            identifier_code="telegram",
            name="Telegram",
            description="Telegram Client bot for integrations with locally installed Telegram application.",
            tags=["Telegram", "Messenger", "Messages", "Communication"],
            functions=[
                Function(
                    identifier_code="unread_messages",
                    name="List unread messages",
                    description="List all new messages from Telegram.",
                    call_examples=[
                        "Read messages",
                        "Is there new messages",
                        "Anything new",
                        "Unread messages",
                        "Messages",
                        "Any messages"
                    ],
                    parameters_set_list=[]
                ),
                Function(
                    identifier_code="send_message",
                    name="Send message",
                    description="Send messenger with Telegram client with active account.",
                    call_examples=["Send message", "Send", "Write", "Write message"],
                    parameters_set_list=[]
                )
            ]
        ),
        Application(
            identifier_code="email",
            name="EMail",
            description="Email integration for managing emaild from GMail.",
            tags=["Mail", "GMail", "Email", "Communication"],
            functions=[
                Function(
                    identifier_code="unread_mails",
                    name="List unread mail",
                    description="Lists all new mail from GMail.",
                    call_examples=[
                        "Read mail",
                        "Read email",
                        "Are there new mails",
                        "Anything new",
                        "Unread mail",
                        "Unread email",
                        "Any mail"
                    ],
                    parameters_set_list=[]
                ),
                Function(
                    identifier_code="send_mail",
                    name="Send mail",
                    description="Sends mail with your GMail account.",
                    call_examples=["Send mail", "Send", "Write", "Write mail"],
                    parameters_set_list=[]
                )
            ]
        ),
        Application(
            identifier_code='timer',
            name='Timer',
            description="Timer",
            tags=["Timer"],
            functions=[
                Function(
                    identifier_code="start_new",
                    name="Start timer",
                    description="Starts timer for specified time.",
                    call_examples=["Remind me in", "Call me in", "Start timer for", "Set timer for"],
                    parameters_set_list=[]
                ),
                Function(
                    identifier_code="disable_all",
                    name="Disable all timers",
                    description="Disables all active timers",
                    call_examples=["Suppress all", "Disable all"],
                    parameters_set_list=[]
                ),
                Function(
                    identifier_code="list",
                    name="List active timers",
                    description="Lists all active timers",
                    call_examples=["List all", "Show all"],
                    parameters_set_list=[]
                )
            ]
        ),
        Application(
            identifier_code="calendar",
            name="Calendar",
            description="Google calendar management",
            tags=["Calendar", "Google Calendar"],
            functions=[
                Function(
                    identifier_code="list",
                    name="List events",
                    description="Shows all events for specified date",
                    call_examples=["List events", "Whats for", "Any events for"],
                    parameters_set_list=[]
                )
            ]
        ),
        Application(
            identifier_code="stopwatch",
            name="Stopwatch",
            description="Stopwatch",
            tags=["Stopwatch"],
            functions=[
                Function(
                    identifier_code="start_new",
                    name="Start stopwatch",
                    description="Starts stopwatch",
                    call_examples=["Start stopwatch", "Launch stopwatch"],
                    parameters_set_list=[]
                )
            ]
        ),
        Application(
            identifier_code="alarm_clock",
            name="Alarm clock",
            description="Alarm clock",
            tags=["Alarm clock"],
            functions=[
                Function(
                    identifier_code="start_new",
                    name="Start alarm clock",
                    description="Starts alarm clock for specified date and time",
                    call_examples=["Start alarm for", "Launch alarm for", "Create alarm for"],
                    parameters_set_list=[]
                ),
                Function(
                    identifier_code="list",
                    name="List active alarms",
                    description="Lists active alarms",
                    call_examples=["List alarms"],
                    parameters_set_list=[]
                ),
                Function(
                    identifier_code="shew_nearest",
                    name="Show nearest alarm",
                    description="Show nearest active alarm clock",
                    call_examples=["Show nearest alarm", "Show next alarm"],
                    parameters_set_list=[]
                ),
            ]
        ),
        Application(
            identifier_code="user_custom_statistics",
            name="Custom User Statistics",
            description=("Tool for tracking custom user-defined metrics. "
                         "Define your own counters, Yes/No questions, configure tracking period (hour, day, week)."),
            tags=["Statistics", "Metrics", "Monitoring", "Counter"],
            functions=[
                Function(
                    identifier_code="increase_counter",
                    name="Increase counter",
                    description="Increases user defined counter",
                    call_examples=["Increase counter", "Add to counter", "Plus to counter"],
                    parameters_set_list=[]
                ),
                Function(
                    identifier_code="decrease_counter",
                    name="Decrease counter",
                    description="Decreases user defined counter",
                    call_examples=["Decrease counter", "Subtract from counter", "Take away from counter",
                                   "Minus from counter"],
                    parameters_set_list=[]
                ),
                Function(
                    identifier_code="show_statistics",
                    name="Show statistics",
                    description="Shows statistics",
                    call_examples=["Show tracking results", "Show", "Monitoring results"],
                    parameters_set_list=[]
                )
            ]
        ),
        Application(
            identifier_code="shortcuts",
            name="Shortcuts",
            description="Defines keyboard shortcuts, that can be triggered by voice",
            tags=["Shortcut", "Keyboard"],
            functions=[
                Function(
                    identifier_code="press_shortcut",
                    name="Press shortcut",
                    description="Fire key-press event.",
                    call_examples=["Press", "Fire", "Click", "Expose"],
                    parameters_set_list=[]
                ),
            ]
        ),
        Application(
            identifier_code="pc_system",
            name="PC System",
            description="Defines an interface to interract with your PC by voice.",
            tags=["PC", "System", "Computer management"],
            functions=[
                Function(
                    identifier_code="sound_up",
                    name="Sound up",
                    description="Increase a sound level on the PC",
                    call_examples=["Louder", "Increase voice", "Increase sound"],
                    parameters_set_list=[]
                ),
                Function(
                    identifier_code="sound_down",
                    name="Sound down",
                    description="Decrease a sound level on the PC",
                    call_examples=["Quieter", "Decrease voice", "Decrease sound"],
                    parameters_set_list=[]
                ),
                Function(
                    identifier_code="mute_sound",
                    name="Mute sound",
                    description="Mutes sound on the PC",
                    call_examples=["Hush", "Quiet", "Silence", "Mute"],
                    parameters_set_list=[]
                ),
                Function(
                    identifier_code="set_sound_level",
                    name="Set sound level",
                    description="Set sound level to a specified value (from 0 to 100).",
                    call_examples=["Set sound"],
                    parameters_set_list=[]
                ),

                Function(
                    identifier_code="brightness_up",
                    name="Brightness up",
                    description="Increase a brightness level on the PC",
                    call_examples=["Brighter", "Increase brightness"],
                    parameters_set_list=[]
                ),
                Function(
                    identifier_code="brightness_down",
                    name="Brightness down",
                    description="Decrease a brightness level on the PC",
                    call_examples=["Darker", "Decrease brightness"],
                    parameters_set_list=[]
                ),
                Function(
                    identifier_code="set_brightness",
                    name="Set brightness level",
                    description="Set sound level to a specified value (from 0 to 100).",
                    call_examples=["Set brightness"],
                    parameters_set_list=[]
                ),
            ]
        ),
        Application(
            identifier_code="app_windows_management",
            name="App windows management",
            description="Voice interface to manage active application windows.",
            tags=["windows"],
            functions=[
                Function(
                    identifier_code="minimize_window",
                    name="Minimize active window",
                    description="Minimizes active application window.",
                    call_examples=["Minimize current window", "Suppress current app", "Hide current window"],
                    parameters_set_list=[]
                ),
                Function(
                    identifier_code="open_window",
                    name="Open window",
                    description="Open one of the minimized but active application window.",
                    call_examples=["Open", "Show", "Maximize window"],
                    parameters_set_list=[]
                ),
            ]
        )
    ])


with open('./test_configs/apps_config.json', 'w') as f:
    json.dump(apps_config_factory().to_dict(), f, indent=4)

