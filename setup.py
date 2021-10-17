from cx_Freeze import setup, Executable
  
executables = [
        Executable(script = "SpaceInvader/main.py", icon = "SpaceInvader/images/icone.ico", base = "Win32GUI" )
]
  
buildOptions = dict( 
        includes = ["random","time","pygame"]
)
  
setup(
    name = "Space Invader",
    version = "1.0.4.16",
    description = "Jeu inspiré des Space Invader développé dans le but du ProjetPrintemps en NSI",
    author = "Louis & Fabien",
    options = dict(build_exe = buildOptions),
    executables = executables
)