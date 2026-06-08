shader_type canvas_item;

uniform float progress : hint_range(0.0, 1.0) = 0.0;
uniform bool from_center = false;

void fragment() {
    vec2 uv = UV - vec2(0.5);

    float dist;
    if (from_center) {
        dist = length(uv);
    } else {
        dist = max(abs(uv.x), abs(uv.y)); // desde las esquinas
    }

    float maxDist = 0.75;

    // Normalizar distancia a [0,1]
    float normDist = dist / maxDist;

    // progress=0 → todo negro | progress=1 → todo transparente
    float alpha = smoothstep(progress - 0.05, progress + 0.05, normDist);

    COLOR = vec4(0.0, 0.0, 0.0, alpha);
}