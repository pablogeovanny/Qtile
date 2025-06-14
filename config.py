"""This script sets the base configuration for Qtile.

It consists of keybindings, layouts, widgets, rules and hooks.
An in depth documentation can be found at:
https://github.com/david35mm/.files/tree/main/.config/qtile
"""

import os
import re
import shutil
import socket
import subprocess
from libqtile import bar, hook, layout, qtile, widget
from typing import List #noqa> F401 
from libqtile.config import EzClick as Click
from libqtile.config import EzDrag as Drag
from libqtile.config import EzKey as Key
from libqtile.config import Group, Rule, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import Spacer, Prompt
from libqtile.widget.prompt import Prompt

#autostart
cmd = [
	"xrandr --output Virtual-1 --mode 1920x1080",
	"setxkbmap es",
	"feh --bg-fill ~/.config/qtile/wall.jpg",
	"picom --no-vsync &",
	"spice-vdagent"
]
for x in cmd:
	os.system(x)

mod = "mod4"
my_term = "alacritty"
my_browser = "firefox"
my_file_manager = "thunar"
target = ""
#my_markdown = "marktext"
#my_music_player = my_term + " --class cmus,cmus -e cmus"
#my_office_suite = "desktopeditors"
#my_pdf_reader = "zathura"
#my_text_editor = "geany"
#my_video_player = "celluloid"
@lazy.function
def update_target(qtile):
	def get_text(text):
		genpolltext = qtile.widgets_map["targettext"]
		genpolltext.update(f" {text}")
		global target
		target = text
	prompt = qtile.widgets_map["prompt"]
	prompt.start_input("", get_text)

mouse = [
    Drag("M-1",
         lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag("M-3",
         lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click("M-2",
          lazy.window.bring_to_front()),
]

# SUPER + FUNCTION KEYS
keys = [
	Key("M-f", lazy.spawn('firefox')),
	Key("M-q", lazy.window.kill()),
	Key("M-t", lazy.spawn(my_term)),
	Key("M-v", lazy.spawn('pavucontrol')),
	Key("M-m", lazy.spawn('thunar')),
#	Key("M-y", lazy.spawncmd()),
	Key("M-y", update_target),
#	Key("M-i", lazy.spawn('echo $(whoami | xsel -ib')),
	Key("M-<return>", lazy.spawn('rofi -show run')),

# SUPER + CTRL + ALT + FUNCTION KEYS
	Key("M-C-A-r", lazy.restart()),
	Key("M-C-A-p", lazy.spawn('poweroff')),
	Key("M-C-A-c", lazy.shutdown(), desc="Quit Qtile"),
	Key("M-C-A-l", lazy.spawn('xtrlock')),
	Key("M-C-A-o", lazy.spawn('reboot')),

# CONTROL + ALT KEYS

# ALT + ... KEYS
	Key("A-f", lazy.window.toggle_fullscreen()),

# CONTROL + SHIFT KEYS

#    Key("C-S-E", lazy.spawn('lxtask')),

# SCREENSHOTS

#    Key([], "Print", lazy.spawn('flameshot full -p ' + home + '/Pictures')),
#    Key([mod2], "Print", lazy.spawn('flameshot full -p ' + home + '/Pictures')),
#    Key([mod2, "shift"], "Print", lazy.spawn('gnome-screenshot -i')),

# MULTIMEDIA KEYS

# INCREASE/DECREASE BRIGHTNESS
	Key("<XF86MonBrightnessUp>", lazy.spawn("brightnessctl s +5%")),
	Key("<XF86MonBrightnessDown>", lazy.spawn("brightnessctl s -5%")),

# INCREASE/DECREASE/MUTE VOLUME
	Key("<XF86AudioMute>", lazy.spawn("amixer -q set Master toggle")),
	Key("<XF86AudioLowerVolume>", lazy.spawn("amixer -q set Master 5%-")),
	Key("<XF86AudioRaiseVolume>", lazy.spawn("amixer -q set Master 5%+")),

	Key("<XF86AudioPlay>", lazy.spawn("playerctl play-pause")),
	Key("<XF86AudioNext>", lazy.spawn("playerctl next")),
	Key("<XF86AudioPrev>", lazy.spawn("playerctl previous")),
	Key("<XF86AudioStop>", lazy.spawn("playerctl stop")),

#    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
#    Key([], "XF86AudioNext", lazy.spawn("mpc next")),
#    Key([], "XF86AudioPrev", lazy.spawn("mpc prev")),
#    Key([], "XF86AudioStop", lazy.spawn("mpc stop")),

# QTILE LAYOUT KEYS
	Key("M-n", lazy.layout.normalize()),
	Key("M-<space>", lazy.next_layout()),

# CHANGE FOCUS
	Key("M-<Up>", lazy.layout.up()),
	Key("M-<down>", lazy.layout.down()),
	Key("M-<left>", lazy.layout.left()),
	Key("M-<right>", lazy.layout.right()),

# RESIZE UP, DOWN, LEFT, RIGHT
	Key("M-C-<Right>",
	lazy.layout.grow_right(),
	lazy.layout.grow(),
	lazy.layout.increase_ratio(), 
	lazy.layout.delete(),
        ),
	Key("M-C-<Left>",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
	Key("M-C-<Up>",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
	Key("M-C-<Down>",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),

# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key("M-S-f", lazy.layout.flip()),

# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key("M-S-<Up>", lazy.layout.shuffle_up()),
    Key("M-S-<Down>", lazy.layout.shuffle_down()),
    Key("M-S-<Left>", lazy.layout.swap_left()),
    Key("M-S-<Right>", lazy.layout.swap_right()),

# TOGGLE FLOATING LAYOUT
    Key("M-S-<space>", lazy.window.toggle_floating()),
#    Key("M-S-j", lazy.layout.shuffle_up(), desc="Swap with previous window"),
#    Key("M-S-k", lazy.layout.shuffle_down(), desc="Swap with next window"),
#    Key("M-j", lazy.group.prev_window(),
#        desc="Focus previous window"),
#    Key("M-k",
#        lazy.group.next_window(),
#        desc="Focus next window"),
#    Key("M-s",
#        lazy.window.toggle_fullscreen(),
#        desc="Fullscreen toogle"),
#    Key("M-w",
#        lazy.window.kill(),
#        desc="Close the window"),
#    Key("M-f",
#        lazy.window.toggle_floating(),
#        desc="Floating toggle"),
#    Key("M-S-f",
#        lazy.layout.flip(),
#        desc="Flip master pane side"),
#    Key("M-S-h",
#        lazy.layout.shrink(),
#        desc="Shrink window size"),
#    Key("M-S-l",
#        lazy.layout.grow(),
#        desc="Expand window size"),
#    Key("M-S-n",
#        lazy.layout.reset(),
#        desc="Normalize all windows size"),
#    Key("M-<Tab>",
#        lazy.next_layout(),
#        desc="Cycle through layouts"),
#    Key("M-h",
#        lazy.layout.shrink_main(),
#        desc="Shrink master pane width"),
#    Key("M-l",
#        lazy.layout.grow_main(),
#        desc="Grow master pane width"),
#    Key("M-n",
#        lazy.layout.normalize(),
#        desc="Normalize all slave windows size"),
#    Key("M-<comma>",
#        lazy.prev_screen(),
#        desc="Focus the previous screen"),
#    Key("M-<period>",
#        lazy.next_screen(),
#        desc="Focus the next screen"),
#    Key("<XF86AudioLowerVolume>",
#        lazy.spawn("pamixer -u -d 5"),
#        desc="Decrease the volume"),
#    Key("<XF86AudioMute>",
#        lazy.spawn("pamixer -t"),
#        desc="Mute toggle"),
#    Key("<XF86AudioRaiseVolume>",
#        lazy.spawn("pamixer -u -i 5"),
#        desc="Increase the volume"),
#    Key("<XF86MonBrightnessDown>",
#        lazy.spawn("brightnessctl set 10%-"),
#        desc="Decrease the brightness"),
#    Key("<XF86MonBrightnessUp>",
#        lazy.spawn("brightnessctl set 10%+"),
#        desc="Increase the brightness"),
#    Key("A-j",
#        lazy.spawn("brightnessctl set 10%-"),
#        desc="Decrease the brightness"),
#    Key("A-k",
#        lazy.spawn("brightnessctl set 10%+"),
#        desc="Increase the brightness"),
#    Key("M-r",
#        lazy.spawn("rofi -show drun"),
#        desc="Run the application launcher"),
#    Key("M-A-r",
#        lazy.spawn("rofi -show run"),
#        desc="Launch the run prompt"),
#    Key("A-<Tab>",
#        lazy.spawn("rofi -show window"),
#        desc="Open the window switcher"),
#    Key("M-<Return>",
#        lazy.spawn(my_term),
#        desc="Launch " + my_term),
#    Key("M-A-i",
#        lazy.spawn(my_browser),
#        desc="Launch " + my_browser),
#    Key("M-e",
#        lazy.spawn(my_file_manager),
#        desc="Launch " + my_file_manager),
#    Key("M-A-d",
#        lazy.spawn(my_markdown),
#        desc="Launch " + my_markdown),
#    Key("M-A-m",
#        lazy.spawn(my_music_player),
#        desc="Launch " + my_music_player),
#    Key("M-A-o",
#        lazy.spawn(my_office_suite),
#        desc="Launch " + my_office_suite),
#    Key("M-A-p",
#        lazy.spawn(my_pdf_reader),
#        desc="Launch " + my_pdf_reader),
#    Key("M-A-t",
#        lazy.spawn(my_text_editor),
#        desc="Launch " + my_text_editor),
#    Key("M-A-v",
#        lazy.spawn(my_video_player),
#        desc="Launch " + my_video_player),
#    Key("M-A-e",
#        lazy.spawn(my_term + " -e vifm"),
#        desc="Launch " + my_term + " -e vifm"),
#    Key("M-A-s",
#        lazy.spawn("spotify"),
#        desc="Launch spotify"),
#    Key("M-A-g",
#        lazy.spawn("steam"),
#        desc="Launch steam"),
]

groups = [
    Group("",
	layout="monadtall",
#          matches=[
#              Match(wm_class=["Brave-browser", "Min"]),]
          ),
    Group(" ",
          layout="max",
#          matches=[
#              Match(wm_class=["Emacs", "Geany", "jetbrains-idea"]),]
          ),
    Group(" ",
          layout="monadtall",
#          matches=[
#              Match(wm_class=["Lxappearance", "Nitrogen"]),]
          ),
    Group(" ",
          layout="max",
          ),
#    Group("chat",
#          layout="max",
#          matches=[
#              Match(wm_class=["TelegramDesktop"]),]
#          ),
    Group(" ",
          layout="monadtall",
#          matches=[
#              Match(wm_class=["cmus", "Geeqie"]),
#              Match(title=["Celluloid"]),
          ),
#    Group("gfx",
#          layout="floating"),
]

for k, group in zip(["1", "2", "3", "4", "5", "6", "7", "8"], groups):
  keys.append(Key("M-" + (k), lazy.group[group.name].toscreen()))
  keys.append(Key("M-S-" + (k), lazy.window.togroup(group.name)))

colours = [
    ["#181b20", "#181b20"],  # Background
    ["#e6e6e6", "#e6e6e6"],  # Foreground
    ["#535965", "#535965"],  # Grey Colour
    ["#e55561", "#e55561"],
    ["#8ebd6b", "#8ebd6b"],
    ["#e2b86b", "#e2b86b"],
    ["#4fa6ed", "#4fa6ed"],
    ["#bf68d9", "#bf68d9"],
    ["#48b0bd", "#48b0bd"],
    ["#e85679", "#e85679"],
]

layout_theme = {
    "border_focus": colours[6],
    "border_normal": colours[2],
    "margin": 4,
    "border_width": 2,
}

layouts = [
    	layout.MonadTall(**layout_theme),
	layout.MonadWide(**layout_theme),
	layout.Max(**layout_theme),
	layout.Floating(**layout_theme),
#	layout.Bsp(**layout_theme),
#	layout.Columns(**layout_theme),
#	layout.Matrix(**layout_theme),
#	layout.RatioTile(**layout_theme),
#	layout.Slice(**layout_theme),
#	layout.Stack(num_stacks=2),
#	layout.Stack(stacks=2, **layout_theme),
#	layout.Tile(shift_windows=True, **layout_theme),
#	layout.VerticalTile(**layout_theme),
#	layout.Zoomy(**layout_theme),
#	layout.MonadTall(**border_args),
]

#prompt = f"{os.environ['USER']}@{socket.gethostname()}: "

widget_defaults = dict(background=colours[0],
                       foreground=colours[1],
                       font="Roboto Nerd Font Regular",
                       fontsize=12,
                       padding=1)

extension_defaults = widget_defaults.copy()

widgets = [
    widget.Sep(foreground=colours[0], linewidth=4),
    widget.Image(
	margin=2,
	fontsize = 14,
        filename="~/.config/qtile/logohitman.png",
        mouse_callbacks=({
            "Button1": lambda: qtile.cmd_spawn("rofi -show drun"),
            "Button3": lambda: qtile.cmd_spawn("rofi -show run"),
	}),
        scale=True),
    widget.Sep(foreground=colours[2],linewidth=1, padding=10),
    widget.GroupBox(
	fontsize = 14,
        active=colours[7],
        inactive=colours[2],
        other_current_screen_border=colours[5],
        other_screen_border=colours[2],
        this_current_screen_border=colours[6],
        this_screen_border=colours[2],
        urgent_border=colours[3],
        urgent_text=colours[3],
        disable_drag=True,
        highlight_method="text",
        invert_mouse_wheel=True,
        margin=2,
        padding=0,
        rounded=True,
        urgent_alert_method="text"),
    widget.Sep(foreground=colours[2], linewidth=1, padding=10),
    widget.CurrentLayout(
	fontsize = 14,
        foreground=colours[6],
        font="Roboto Nerd Font Bold"),
#    widget.Systray(
#        icon_size=14,
#        padding=4),
#    widget.Cmus(
#        noplay_color=colours[2],
#        play_color=colours[1]),
    widget.Sep(foreground=colours[2], linewidth=1, padding=10),
    widget.WindowName(
        max_chars=75,
	fontsize = 14),
    # widget.Backlight(
    #     foreground=colours[3],
    #     foreground_alert=colours[3],
    #     format=" {percent:2.0%}",
    #     backlight_name="amdgpu_bl0", # ls /sys/class/backlight/
    #     change_command="brightnessctl set {0}%",
    #     step=10),
    widget.Prompt(
        prompt="Set target: ",
        foreground = colours[9],
	),
    widget.TextBox(
	name = "targettext",
        foreground = colours[9],
	fontsize = 14,
#	fmt = " {}",
#	func = pollfunc,
#	func = lambda: target
	mouse_callbacks = {
	"Button1": lambda: subprocess.run(["xsel", "-ib"], input=target.encode("utf-8"), check=True)
	}
        ),
    widget.Sep(foreground=colours[0],linewidth=1,padding=10),
    widget.GenPollCommand(
	name = "vpn_ip",
        foreground = colours[4],
	fontsize = 14,
	fmt = " {}",
	cmd = "ip address | grep tun0 | grep inet | awk '{print $2}' | cut -d '/' -f 1",
	shell = True,
        update_interval = 2.0,
        mouse_callbacks = {
            "Button1": lambda: subprocess.check_output("ip address | grep tun0 | grep inet | awk '{print $2}' | cut -d '/' -f 1 | tr -d '\n' | xsel -ib", shell=True, text=True)
        },
        ),
    widget.Sep(foreground=colours[2],linewidth=1,padding=10),
    widget.GenPollCommand(
	name = "ip",
        foreground = colours[5],
	fontsize = 14,
	fmt = " {}",
	cmd = "hostname -I | awk '{print $1}'",
	shell = True,
        update_interval = 2.0,
        mouse_callbacks = {
		"Button1" : lambda: subprocess.check_output("hostname -I | awk '{print $1}' | tr -d '\n' | xsel -ib", shell=True, text=True),
        },
        ),
    widget.Sep(foreground=colours[2],linewidth=1,padding=10),
    widget.Net(
        foreground = colours[6],
	fontsize = 14,
	prefix = "M",
	format = "{down:4.2f}{down_suffix}   {up:4.2f}{up_suffix}",
    #     interface = "enp1s0"
	),
    widget.Sep(foreground=colours[2],linewidth=1,padding=10),
    widget.CPU(
        foreground=colours[5],
	fontsize = 14,
        format=" {load_percent}%",
        mouse_callbacks={
            "Button1": lambda: qtile.cmd_spawn(my_term + " -e htop"),
        },
        update_interval=1.0),
    widget.Sep(foreground=colours[2], linewidth=1, padding=10),
    widget.Memory(
        foreground=colours[7],
	fontsize = 14,
        format=" {MemUsed:.1f}{mm}/{MemTotal:.1f}{mm}",
mouse_callbacks={
            "Button1": lambda: qtile.cmd_spawn(my_term + " -e htop"),
        },
	measure_mem='G',
        update_interval=1.0),
    widget.Sep(
        foreground=colours[2],
        linewidth=1,
        padding=10),
#    widget.CheckUpdates(
#        colour_have_updates=colours[5],
#        colour_no_updates=colours[5],
#        custom_command="checkupdates",
#        # custom_command="dnf updateinfo -q --list",
#        display_format=" {updates} Updates",
#        no_update_string=" Up to date!",
#        mouse_callbacks=({
#            "Button1": lambda: qtile.cmd_spawn(os.path.expanduser(
#                "~/.config/scripts/update_system.sh")),
#            "Button3": lambda: qtile.cmd_spawn(os.path.expanduser(
#                "~/.config/scripts/check_updates.sh")),
#        }),
#        update_interval=900),
#    widget.Sep(
#        foreground=colours[2],
#        linewidth=1,
#        padding=10),
    widget.Volume(
        foreground=colours[8],
	fontsize = 14,
        fmt=" {}",
        update_interval=0.1,
        volume_app="pavucontrol",
        step=5,
	limit_max_volume="true"
	),
#    widget.Sep(foreground=colours[2],linewidth=1,padding=10),
#    widget.Battery(
#        foreground=colours[4],
#	fontsize = 14,
#        format="{char} {percent:2.0%}",
#        charge_char="",
#        discharge_char="",
#        empty_char="",
#        full_char="",
#        unknown_char="",
#        low_foreground=colours[3],
#        low_percentage=0.15,
#        show_short_text=False,
#        notify_below=15,
#	update_interval=1,
#	scroll_interval=0.1
#	),
    widget.Sep(foreground=colours[2], linewidth=1, padding=10),
    widget.Clock(
        foreground=colours[1],
	fontsize = 14,
        format=" %d %b %H:%M "),
    # widget.StockTicker(
    #     apikey="AESKWL5CJVHHJKR5",
    #     url="https://www.alphavantage.co/query?"),
]

def status_bar(widgets):
  return bar.Bar(widgets, 25, opacity=0.9, margin=2, border_width=0)

screens = [
    Screen(
        top=status_bar(widgets),
#        wallpaper="/usr/share/wallpapers/deepin/Overlooking_by_Lance_Asper.jpg",
        wallpaper_mode="stretch",
	),
]

connected_monitors = (subprocess.run(
    "xrandr | busybox grep 'connected' | busybox cut -d' ' -f2",
    check=True,
    shell=True,
    stdout=subprocess.PIPE,
).stdout.decode("UTF-8").split("\n")[:-1].count("connected"))

if connected_monitors > 1:
  for i in range(1, connected_monitors):
    screens.append(
        Screen(
            top=status_bar(widgets),
#            wallpaper="/usr/share/wallpapers/deepin/Overlooking_by_Lance_Asper.jpg",
    wallpaper_mode="stretch"))

auto_fullscreen = True
auto_minimize = True
bring_front_click = False
cursor_warp = False
dgroups_app_rules = []
dgroups_key_binder = None
floating_layout = layout.Floating(
    **layout_theme,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(title="Authentication"),
        Match(title="branchdialog"),
        Match(title="Chat"),
        Match(title="pinentry"),
        Match(title="Polls"),
        Match(wm_class="Arandr"),
        Match(wm_class="Blueman-adapters"),
        Match(wm_class="Blueman-manager"),
        Match(wm_class="confirm"),
        Match(wm_class="confirmreset"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="error"),
        Match(wm_class="file_progress"),
        Match(wm_class="Gnome-screenshot"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="notification"),
        Match(wm_class="Pavucontrol"),
        Match(wm_class="splash"),
        Match(wm_class="ssh-askpass"),
        Match(wm_class="toolbar"),
    ])
focus_on_window_activation = "smart"
follow_mouse_focus = True
reconfigure_screens = True

# pylint: disable=consider-using-with
@hook.subscribe.restart
def delete_cache():
  shutil.rmtree(os.path.expanduser("~/.config/qtile/__pycache__"))

@hook.subscribe.shutdown
def stop_apps():
  delete_cache()
  qtile.cmd_spawn(["killall", "dunst", "lxpolkit", "picom", "udiskie"])

#@hook.subscribe.startup_once
#def start_apps():
#  qtile.cmd_spawn(["dunst"])
#  qtile.cmd_spawn(["lxpolkit"])
#  qtile.cmd_spawn(["picom", "-b"])
#  qtile.cmd_spawn(["udiskie", "-asn", "-f", "pcmanfm-qt"])

wmname = "LG3D"
