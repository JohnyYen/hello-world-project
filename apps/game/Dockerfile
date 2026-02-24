FROM barichello/godot-ci:4.4.1

WORKDIR /project

COPY . .

RUN godot --export "Linux/X11" build/linux/game.x86_64
