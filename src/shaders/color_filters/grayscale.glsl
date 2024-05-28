// Grayscale shader

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec2 uv = fragCoord.xy / iResolution.xy;
//    vec3 col = texture(iChannel4, uv).xyz;
    vec3 col = vec3(0.0);
    float gray = dot(col, vec3(0.299, 0.587, 0.114));
//    float trans = min((7.0 - iTime) * 0.6, 0.9);

    fragColor = vec4(vec3(gray), clamp(1.0, 0.0, iTime));
}
