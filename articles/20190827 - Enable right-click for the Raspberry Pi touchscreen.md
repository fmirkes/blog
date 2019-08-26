## Enable right-click for the Raspberry Pi touchscreen

**(Yes, even under Raspbian 10 Buster)**
> tl;dr
>
> 1. Install [evdev-right-click-emulation](https://github.com/PeterCxy/evdev-right-click-emulation)
>
> 2. Load the *uinput* kernel module
>
> 3. Make sure that you have access to /dev/uinput and /dev/input
>
> 4. Run evdev-right-click-emulation

<summary>
Finally I got my hands on a new Raspberry Pi 4, and I wanted to use the official 7" touchscreen with it. There was only one problem: The right click didn't work.

There are multiple ways floating around the web to enable it (e.g. in the [official forums][1]), but none of them worked for me under Raspbian 10.
Even the config files in */usr/share/X11/xorg.conf.d* look like it should work out of the box.

After a long frustrating search I found a solution: 
A small program called [evdev-right-click-emulation][2].
</summary>

[1]: https://www.raspberrypi.org/forums/viewtopic.php?t=138575
[2]: https://github.com/PeterCxy/evdev-right-click-emulation

### Installation of evdev-rce
Installation is pretty straight forward:

~~~sh
sudo apt install build-essential libevdev2 libevdev-dev
git clone 'https://github.com/PeterCxy/evdev-right-click-emulation.git'
cd 'evdev-right-click-emulation'
make all
sudo cp 'out/evdev-rce' '/usr/local/bin/'
chmod +x '/usr/local/bin/evdev-rce'
~~~

You enable right-clicking by running it via `sudo evdev-rce` from a graphical terminal.

Now there is the next problem: How do you enable autostart for normal users without entering a password? 
Of course there are different ways like setting the setuid bit, or using the *NOPASSWD* directive in */etc/sudoers*.

But why run it as *root* when you can run it as normal user?

### Run evdev-rce as normal user 
First of all your user (usually *pi*) needs access to the input devices in */dev/input*:

~~~sh
sudo usermod -G 'input' -a pi
~~~

*evdev-rce* uses the kernel module [uinput](https://www.kernel.org/doc/html/latest/input/uinput.html), which is used to create virtual input devices. It has to be automatically loaded at boot:
~~~sh
echo 'uinput' | sudo tee -a /etc/modules
~~~

The *uinput* device can be found under */dev/uinput*. By default only root is allowed to access it. We are going to change that with a custom *udev* rule:

~~~sh
# /etc/udev/rules.d/99-uinput.rules

KERNEL=="uinput", MODE="0660", GROUP="input"
~~~

~~~sh
sudo udevadm control --reload-rules
sudo udevadm trigger
~~~

After a re-login, you should be able to run *evdev-rce* as normal user.

### Startup evdev-rce on login
To start *evdev-rce* on login just create the following file:
~~~sh
# $HOME/.config/autostart/evdev-rce.desktop

[Desktop Entry]
Version=1.0
Type=Application
Name=evdev-rce
GenericName=Enable long-press-to-right-click gesture
Exec=env LONG_CLICK_INTERVAL=500 LONG_CLICK_FUZZ=50 /usr/local/bin/evdev-rce
Terminal=true
StartupNotify=false
~~~
