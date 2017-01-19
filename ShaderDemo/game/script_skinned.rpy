
image doll = LiveComposite(
    (800, 1000),
    (0, 0), "doll base.png",
    (249, 318), "doll skirt.png",
    #(0, 0), "doll lforearm.png",
    #(0, 0), "doll larm.png",
    #(0, 0), "doll lhand.png",
    #(0, 0), "doll hair.png",
)

screen skinnedScreen(name, pixelShader, textures={}, uniforms={}, update=None, args=None, xalign=0.5, yalign=0.5):
    modal True
    add ShaderDisplayable(shader.MODE_SKINNED, name, shader.VS_SKINNED, pixelShader, textures, uniforms, None, update, args):
        xalign xalign
        yalign yalign
        #rotate 45

    frame:
        xpadding 10
        ypadding 10


        vbox:
            spacing 10
            #xmaximum 150
            #xminimum 150
            text name

            text "Toggles":
                size 15

            textbutton "Wireframes" action [ToggleDict(editorSettings, "wireframe"), RestartStatement()]
            textbutton "Image areas" action [ToggleDict(editorSettings, "imageAreas"), RestartStatement()]
            textbutton "Bones" action [ToggleDict(editorSettings, "pivots"), RestartStatement()]
            textbutton "Bone names" action [ToggleDict(editorSettings, "names"), RestartStatement()]
            textbutton "Debug animate" action [ToggleDict(editorSettings, "debugAnimate"), RestartStatement()]

            text "Actions":
                size 15

            textbutton "Reload" action Confirm("Are you sure you want to reload?", Jump("start_skinned"))
            #textbutton "Save" action Confirm("Are you sure you want to save?", Function(editSave))
            textbutton "Save rig" action SetVariable("saveRig", True)

init python:
    from shader import skinnededitor

    #config.keymap["input_delete"] = []
    config.keymap["game_menu"].remove("mouseup_3")
    config.keymap["hide_windows"].remove("h")
    config.keymap["screenshot"].remove("s")

    editorSettings = {
        "wireframe": True,
        "imageAreas": True,
        "pivots": True,
        "names": False,
        "debugAnimate": False,
    }

    saveRig = False
    rigFile = "bones.rig"

    def userInput(prompt, *args):
        #TODO Exclude invalid characters...
        return renpy.invoke_in_new_context(renpy.input, prompt, *args)

    def notify(text):
        renpy.notify(text)

    def editUpdate(context):
        global saveRig, rigFile

        editor = skinnededitor.SkinnedEditor(context, editorSettings)
        editor.update()

        if saveRig:
            saveRig = False
            fileName = userInput("Save rig as...", rigFile)
            if fileName:
                if not fileName.strip().lower().endswith(".rig"):
                    fileName = fileName + ".rig"
                editor.saveSkeletonToFile(fileName)
                notify("Rig saved to '%s'" % fileName)
                rigFile = fileName


label start_skinned:
label main_menu: #TODO For fast testing
    $ _controllerContextStore._clear()

    call screen skinnedScreen("doll", shader.PS_SKINNED, {"tex1": "amy influence"},
        update=editUpdate, args={"rigFile": rigFile}, _tag="amy", _layer="amy") #nopredict

    "The End"
