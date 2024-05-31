path_tracing_fragment_shader = """
#version 330 core
out vec4 FragColor;
in vec3 fragPos;
uniform vec3 sphereCenter;

vec3 rayDirection(vec2 uv, vec3 ro, vec3 rd)
{
    vec3 forward = normalize(rd);
    vec3 right = normalize(cross(forward, vec3(0.0, 1.0, 0.0)));
    vec3 up = cross(right, forward);
    vec3 direction = normalize(forward + uv.x * right + uv.y * up);
    return direction;
}

bool intersectSphere(vec3 ro, vec3 rd, vec3 sphereCenter, float sphereRadius, out float t)
{
    vec3 oc = ro - sphereCenter;
    float a = dot(rd, rd);
    float b = 2.0 * dot(oc, rd);
    float c = dot(oc, oc) - sphereRadius * sphereRadius;
    float discriminant = b * b - 4.0 * a * c;
    if (discriminant < 0.0) {
        t = -1.0;
        return false;
    } else {
        t = (-b - sqrt(discriminant)) / (2.0 * a);
        return true;
    }
}

vec3 calculateNormal(vec3 p, vec3 sphereCenter)
{
    return normalize(p - sphereCenter);
}

float rand(vec2 co)
{
    return fract(sin(dot(co.xy, vec2(12.9898, 78.233))) * 43758.5453);
}

void main()
{
    vec3 ro = vec3(0.0, 0.0, 5.0);  // Ray origin
    vec3 rd = rayDirection(fragPos.xy, ro, vec3(0.0, 0.0, -1.0));  // Ray direction

    float sphereRadius = 1.0;
    float t;
    vec3 color = vec3(0.0);
    int samples = 50;

    for (int i = 0; i < samples; ++i)
    {
        if (intersectSphere(ro, rd, sphereCenter, sphereRadius, t)) {
            vec3 hitPoint = ro + t * rd;
            vec3 normal = calculateNormal(hitPoint, sphereCenter);
            vec3 lightDir = normalize(vec3(-1.0, -1.0, -1.0));
            float diff = max(dot(normal, lightDir), 0.0);
            color += diff;
        }
        ro += rd * t;
        rd = rayDirection(vec2(rand(ro.xy), rand(ro.yz)), ro, rd);
    }

    FragColor = vec4(color / float(samples), 1.0);
}
"""