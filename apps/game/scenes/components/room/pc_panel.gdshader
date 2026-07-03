shader_type canvas_item;

uniform vec4 center_color : source_color = vec4(0.06, 0.06, 0.1, 0.0);
uniform vec4 edge_color : source_color = vec4(0.06, 0.06, 0.1, 0.6);
uniform float radius : hint_range(0.0, 1.0) = 0.5;

void fragment() {
    vec2 center = vec2(0.5, 0.5);
    float dist = distance(UV, center);
    float t = smoothstep(0.0, radius, dist);
    COLOR = mix(center_color, edge_color, t);
}