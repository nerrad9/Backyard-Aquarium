-- screens.logo

local composer = require ("composer")       
local scene = composer.newScene()          


local mainGroup         

local tmr     


local function cleanUp()

        timer.cancel(tmr)
        tmr = nil
    

end

local function changeScene()
    composer.gotoScene( "screens.mainMenu", "crossFade", 1500 )
end

function scene:create( event )
    local mainGroup = self.view        

    local loadingLogo = display.newImageRect( "assets/logo.png", 1200, 2200 ) 
    loadingLogo.x = display.contentCenterX    
    loadingLogo.y = display.contentCenterY    
    mainGroup:insert(loadingLogo)         


end


function scene:show( event )
    local phase = event.phase

    if ( phase == "will" ) then         

    elseif ( phase == "did" ) then      
        
        tmr = timer.performWithDelay( 4000, changeScene, 1 )        

     
    end
end


function scene:hide( event )
    local phase = event.phase

    if ( phase == "will" ) then       

        cleanUp()       

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
