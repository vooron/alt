from text_to_command.choices_value_provider import ChoicesValueProvider, ChoiceValue
from text_to_command.configuration_units import SkillsConfiguration, SkillConfiguration, SkillFunction
from text_to_command.parameter_value_provider import ConstantParameterValueProvider
from text_to_command.parameters import TextParameter, TimeUnitParameter, IntegerParameter


def apps_config_factory():
    return SkillsConfiguration([
        SkillConfiguration(
            id="telegram",
            name="Telegram",
            description="Telegram Client bot for integrations with locally installed Telegram application.",
            tags=["Telegram", "Messenger", "Messages", "Communication"],
            functions=[
                SkillFunction(
                    id="unread_messages",
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
                    parameters=[]
                ),
                SkillFunction(
                    id="send_message",
                    name="Send message",
                    description="Send messenger with Telegram client with active account.",
                    call_examples=["Send message", "Send", "Write", "Write message"],
                    parameters=[
                        TextParameter(
                            id="message",
                            name="Message"
                        ),
                        TextParameter(
                            id="contact",
                            name="Contact",
                            choices=ChoicesValueProvider(values=[], is_lazy=True)
                        )
                    ]
                )
            ]
        ),
        SkillConfiguration(
            id="email",
            name="EMail",
            description="Email integration for managing emaild from GMail.",
            tags=["Mail", "GMail", "Email", "Communication"],
            functions=[
                SkillFunction(
                    id="unread_mails",
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
                    parameters=[]
                ),
                SkillFunction(
                    id="send_mail",
                    name="Send mail",
                    description="Sends mail with your GMail account.",
                    call_examples=["Send mail", "Send", "Write", "Write mail"],
                    parameters=[
                        TextParameter(
                            id="message",
                            name="Message"
                        ),
                        TextParameter(
                            id="email",
                            name="email",
                            choices=ChoicesValueProvider(values=[], is_lazy=True)
                        )
                    ]
                )
            ]
        ),
        SkillConfiguration(
            id='timer',
            name='Timer',
            description="Timer",
            tags=["Timer"],
            functions=[
                SkillFunction(
                    id="start_new",
                    name="Start timer",
                    description="Starts timer for specified time.",
                    call_examples=["Remind me in", "Call me in", "Start timer for", "Set timer for"],
                    parameters=[
                        TimeUnitParameter(
                            id="timeunit",
                            name="Time Unit"
                        )
                    ]
                ),
                SkillFunction(
                    id="disable_all",
                    name="Disable all timers",
                    description="Disables all active timers",
                    call_examples=["Suppress all", "Disable all"],
                    parameters=[]
                ),
                SkillFunction(
                    id="list",
                    name="List active timers",
                    description="Lists all active timers",
                    call_examples=["List all", "Show all"],
                    parameters=[]
                )
            ]
        ),
        SkillConfiguration(
            id="calendar",
            name="Calendar",
            description="Google calendar management",
            tags=["Calendar", "Google Calendar"],
            functions=[
                SkillFunction(
                    id="list",
                    name="List events",
                    description="Shows all events for specified date",
                    call_examples=["List events", "Whats for", "Any events for"],
                    parameters=[]
                )
            ]
        ),
        SkillConfiguration(
            id="stopwatch",
            name="Stopwatch",
            description="Stopwatch",
            tags=["Stopwatch"],
            functions=[
                SkillFunction(
                    id="start_new",
                    name="Start stopwatch",
                    description="Starts stopwatch",
                    call_examples=["Start stopwatch", "Launch stopwatch"],
                    parameters=[]
                )
            ]
        ),
        SkillConfiguration(
            id="alarm_clock",
            name="Alarm clock",
            description="Alarm clock",
            tags=["Alarm clock"],
            functions=[
                SkillFunction(
                    id="start_new",
                    name="Start alarm clock",
                    description="Starts alarm clock for specified date and time",
                    call_examples=["Start alarm for", "Launch alarm for", "Create alarm for"],
                    parameters=[]  # TODO: add time and datetime params
                ),
                SkillFunction(
                    id="list",
                    name="List active alarms",
                    description="Lists active alarms",
                    call_examples=["List alarms"],
                    parameters=[]
                ),
                SkillFunction(
                    id="show_nearest",
                    name="Show nearest alarm",
                    description="Show nearest active alarm clock",
                    call_examples=["Show nearest alarm", "Show next alarm"],
                    parameters=[]
                ),
            ]
        ),
        SkillConfiguration(
            id="user_custom_statistics",
            name="Custom User Statistics",
            description=("Tool for tracking custom user-defined metrics. "
                         "Define your own counters, Yes/No questions, configure tracking period (hour, day, week)."),
            tags=["Statistics", "Metrics", "Monitoring", "Counter"],
            functions=[
                SkillFunction(
                    id="increase_counter",
                    name="Increase counter",
                    description="Increases user defined counter",
                    call_examples=["Increase counter", "Add to counter", "Plus to counter"],
                    parameters=[
                        IntegerParameter(
                            id="value",
                            name="Value",
                            default=ConstantParameterValueProvider(1),
                            min_value=1
                        )
                    ]
                ),
                SkillFunction(
                    id="decrease_counter",
                    name="Decrease counter",
                    description="Decreases user defined counter",
                    call_examples=["Decrease counter", "Subtract from counter", "Take away from counter",
                                   "Minus from counter"],
                    parameters=[
                        IntegerParameter(
                            id="value",
                            name="Value",
                            default=ConstantParameterValueProvider(1),
                            min_value=1
                        )
                    ]
                ),
                SkillFunction(
                    id="show_statistics",
                    name="Show statistics",
                    description="Shows statistics",
                    call_examples=["Show tracking results", "Show", "Monitoring results"],
                    parameters=[]
                )
            ]
        ),
        SkillConfiguration(
            id="shortcuts",
            name="Shortcuts",
            description="Defines keyboard shortcuts, that can be triggered by voice",
            tags=["Shortcut", "Keyboard"],
            functions=[
                SkillFunction(
                    id="press_shortcut",
                    name="Press shortcut",
                    description="Fire key-press event.",
                    call_examples=["Press", "Fire", "Click", "Expose"],
                    parameters=[
                        TextParameter(
                            id="shortcut",
                            name="Shortcut",
                            choices=ChoicesValueProvider(
                                values=[
                                    ChoiceValue(
                                        label="Save",
                                        value="save"
                                    ),
                                    ChoiceValue(
                                        label="Exit",
                                        value="exit"
                                    ),
                                    ChoiceValue(
                                        label="Enter",
                                        value="enter"
                                    )
                                ],
                                is_lazy=True
                            )
                        )
                    ]
                ),
            ]
        ),
        SkillConfiguration(
            id="pc_system",
            name="PC System",
            description="Defines an interface to interact with your PC by voice.",
            tags=["PC", "System", "Computer management"],
            functions=[
                SkillFunction(
                    id="sound_up",
                    name="Sound up",
                    description="Increase a sound level on the PC",
                    call_examples=["Louder", "Increase voice", "Increase sound"],
                    parameters=[
                        IntegerParameter(
                            id="value",
                            name="Value",
                            default=ConstantParameterValueProvider(5),
                            min_value=1,
                            max_value=100
                        )
                    ]
                ),
                SkillFunction(
                    id="sound_down",
                    name="Sound down",
                    description="Decrease a sound level on the PC",
                    call_examples=["Quieter", "Decrease voice", "Decrease sound"],
                    parameters=[
                        IntegerParameter(
                            id="value",
                            name="Value",
                            default=ConstantParameterValueProvider(5),
                            min_value=1,
                            max_value=100
                        )
                    ]
                ),
                SkillFunction(
                    id="mute_sound",
                    name="Mute sound",
                    description="Mutes sound on the PC",
                    call_examples=["Hush", "Quiet", "Silence", "Mute"],
                    parameters=[]
                ),
                SkillFunction(
                    id="set_sound_level",
                    name="Set sound level",
                    description="Set sound level to a specified value (from 0 to 100).",
                    call_examples=["Set sound"],
                    parameters=[
                        IntegerParameter(
                            id="value",
                            name="Value",
                            min_value=0,
                            max_value=100
                        )
                    ]
                ),

                SkillFunction(
                    id="brightness_up",
                    name="Brightness up",
                    description="Increase a brightness level on the PC",
                    call_examples=["Brighter", "Increase brightness"],
                    parameters=[
                        IntegerParameter(
                            id="value",
                            name="Value",
                            default=ConstantParameterValueProvider(5),
                            min_value=1,
                            max_value=100
                        )
                    ]
                ),
                SkillFunction(
                    id="brightness_down",
                    name="Brightness down",
                    description="Decrease a brightness level on the PC",
                    call_examples=["Darker", "Decrease brightness"],
                    parameters=[
                        IntegerParameter(
                            id="value",
                            name="Value",
                            default=ConstantParameterValueProvider(5),
                            min_value=1,
                            max_value=100
                        )
                    ]
                ),
                SkillFunction(
                    id="set_brightness",
                    name="Set brightness level",
                    description="Set sound level to a specified value (from 0 to 100).",
                    call_examples=["Set brightness"],
                    parameters=[
                        IntegerParameter(
                            id="value",
                            name="Value",
                            min_value=0,
                            max_value=100
                        )
                    ]
                ),
            ]
        ),
        SkillConfiguration(
            id="app_windows_management",
            name="App windows management",
            description="Voice interface to manage active application windows.",
            tags=["windows"],
            functions=[
                SkillFunction(
                    id="minimize_window",
                    name="Minimize active window",
                    description="Minimizes active application window.",
                    call_examples=["Minimize current window", "Suppress current app", "Hide current window"],
                    parameters=[]
                ),
                SkillFunction(
                    id="open_window",
                    name="Open window",
                    description="Open one of the minimized but active application window.",
                    call_examples=["Open", "Show", "Maximize window"],
                    parameters=[
                        TextParameter(
                            id="application",
                            name="Application",
                            choices=ChoicesValueProvider(
                                values=[], is_lazy=True
                            )
                        )
                    ]
                ),
            ]
        )
    ])
