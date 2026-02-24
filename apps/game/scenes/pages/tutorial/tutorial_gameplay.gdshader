shader_type canvas_item;

uniform vec2 highlight_pos;
uniform vec2 highlight_size;

void fragment() {
    vec2 p = (UV - highlight_pos) * vec2(textureSize(TEXTURE, 0));
    if (abs(p.x) < highlight_size.x && abs(p.y) < highlight_size.y) {
        COLOR.a = 0.0; // zona visible
    } else {
        COLOR = vec4(0,0,0,0.6); // oscurecido
    }
}
