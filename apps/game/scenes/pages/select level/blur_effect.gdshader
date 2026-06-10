shader_type canvas_item;

uniform float blur_amount : hint_range(0.0, 5.0) = 2.0;
uniform float mix_amount : hint_range(0.0, 1.0) = 0.3;
uniform vec4 tint_color : source_color = vec4(0.06, 0.06, 0.1, 1.0);
uniform sampler2D SCREEN_TEXTURE: hint_screen_texture, filter_linear_mipmap;

void fragment() {
    vec4 blurred = textureLod(SCREEN_TEXTURE, SCREEN_UV, blur_amount);
    vec4 tinted = mix(blurred, tint_color, mix_amount);
    COLOR = tinted;
}