//#version 330

//out vec4 fragColor;

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 uv = fragCoord.xy / iResolution.xy;
    uv *= 1.0 - uv.yx;

    float vig = uv.x * uv.y * 15.0;
    float vig_pow = 0.15 * abs(sin(iTime)) + 0.25;
    vig_pow *= max(1.0 - iTimeDelta / 70.0, 0.0);

    vig = pow(vig, vig_pow);

    vec3 red_color = vec3(1.0, 0.0, 0.0);

    //    fragColor = vec4(vig);
    fragColor = vec4(red_color, max(1 - vig * 2, 0));
}