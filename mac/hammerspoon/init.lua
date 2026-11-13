-- Global shortcuts. Keep in sync with the logical actions of bin/super.py.
-- Hammerspoon hotkeys use an event tap, so they also see the key events that
-- Deskflow synthesizes on this Mac (Karabiner cannot see those).

require("hs.ipc")
hs.console.clearConsole()

local home = os.getenv("HOME")

local function showEmacs()
    hs.execute("PATH=/opt/homebrew/bin:/usr/bin:/bin " .. home .. "/bin/e", false)
end

local function showKitty()
    hs.application.launchOrFocus("kitty")
end

-- Option+` : show Emacs (like super+`).
-- Bound by raw key code, because key names depend on the active input source.
-- 50 = the ANSI grave key; 10 = the ISO key left of 1 (Karabiner calls it
-- non_us_backslash).
hs.hotkey.bind({"alt"}, 50, showEmacs)
hs.hotkey.bind({"alt"}, 10, showEmacs)

-- F13 : show kitty (like super.py term). Menu key sent by Deskflow arrives as F13.
hs.hotkey.bind({}, "f13", showKitty)

-- Built-in keyboard: tapping Right Option alone shows kitty. Holding it, or
-- using it with another key, still works as a normal Option modifier.
local rightOptionKeyCode = hs.keycodes.map["rightalt"]
local rightOptionDown = false
local rightOptionUsed = false

rightOptionTap = hs.eventtap.new(
    {hs.eventtap.event.types.flagsChanged, hs.eventtap.event.types.keyDown},
    function(event)
        local t = event:getType()
        if t == hs.eventtap.event.types.keyDown then
            if rightOptionDown then rightOptionUsed = true end
        elseif event:getKeyCode() == rightOptionKeyCode then
            local flags = event:getFlags()
            if flags.alt and not rightOptionDown then
                rightOptionDown = true
                rightOptionUsed = false
            elseif rightOptionDown and not flags.alt then
                rightOptionDown = false
                if not rightOptionUsed then showKitty() end
            end
        end
        return false
    end)
rightOptionTap:start()

hs.alert.show("Hammerspoon config loaded")
