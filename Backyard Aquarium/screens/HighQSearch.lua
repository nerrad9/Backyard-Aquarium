-- screens.mainMenu

local composer = require ("composer")      
local scene = composer.newScene()          

local widget = require ("widget")			
											

local mainGroup        


local function onButtonRelease (event)		
	if ( event.phase == "began" ) then
		print "event began"
	elseif ( event.phase == "moved" ) then
		print "event moved"
    elseif ( event.phase == "ended" or event.phase == "cancelled" ) then 		
    	print "event ended"

        if ( event.target.id == "searchNearby" ) then
            composer.gotoScene( "screens.test", "crossFade", 1000 )
        elseif ( event.target.id == "credits" ) then
            composer.gotoScene( "screens.creditScreen", "crossFade", 1000 )
        end
    end
    return true 		

end

function scene:create( event )
    local mainGroup = self.view        


   
    local menubg = display.newImageRect( "assets/HighQ.png", 900,1400 )
    menubg.x = display.contentCenterX
    menubg.y = 600
    mainGroup:insert(menubg)

     local Search = display.newImageRect( "assets/testingfish.png", 350, 200 )
    Search.x = display.contentCenterX 
    Search.y = 1300  
    mainGroup:insert(Search)

    local buttonsearchNearby = widget.newButton{		
        id = "searchNearby",		
        label = "",
        labelColor = { default = { 1, 1, 1 }, over = { 0, 0, 0 } },
   
        width = 372,
        height = 158,
        onEvent = onButtonRelease	
    }
    buttonsearchNearby.x = display.contentCenterX
    buttonsearchNearby.y = 1300
    mainGroup:insert(buttonsearchNearby)


    local buttonCredits = widget.newButton{	
        id = "credits",			
        label = "CREDITS",
        font = native.systemFontBold,
        fontSize = 40,
        labelColor = { default = { 1, 1, 1 }, over = { 0, 0, 0 } },
        textOnly = true,	
        width = 250,
        height = 92,
        onEvent = onButtonRelease		
    }
    buttonCredits.x = 600
    buttonCredits.y = 20
    mainGroup:insert(buttonCredits)
end



function scene:show( event )
    local phase = event.phase

    if ( phase == "will" ) then        

    elseif ( phase == "did" ) then   

 
    	composer.removeScene( "screens.gameLevel" )		
    	composer.removeScene( "screens.creditScreen" )	
    end
end


function scene:hide( event )
    local phase = event.phase

    if ( phase == "will" ) then      

    elseif ( phase == "did" ) then   
    end
end

function scene:destroy( event )

end


scene:addEventListener( "create", scene )
scene:addEventListener( "show", scene )
scene:addEventListener( "hide", scene )
scene:addEventListener( "destroy", scene )

return scene

