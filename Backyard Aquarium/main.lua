-- Project: backyard aquarium
--
-- Date: 10/8/2023
--
-- Version: 0.1
--Author: Aliyah Midgett
-- Edited file: Corona SDK Reference Project Template
-- Original File Author: Serkan Aksit -> https://github.com/sekodev -> https://twitter.com/sekodev http://sleepybugstudios.com -> https://www.facebook.com/sleepybugstudios
--
-- Tools: Visual Studio Code with Corona Editor 
--
-- Update History:
-- 0.1 - Initial release
--
-- Please refer to sources below for more and up-to-date information
-- Corona SDK Docs: http://docs.coronalabs.com
-- Lua docs: http://www.lua.org/docs.html



local composer = require ("composer")		


composer.setVariable("variableString", "Game Level")
composer.setVariable("fontSize", 64)


composer.gotoScene("screens.logo", "crossFade", 1000)