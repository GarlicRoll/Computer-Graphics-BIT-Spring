ray_tracing_fragment_shader = """
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

void main()
{
    vec3 ro = vec3(0.0, 0.0, 5.0);  // Ray origin
    vec3 rd = rayDirection(fragPos.xy, ro, vec3(0.0, 0.0, -1.0));  // Ray direction

    float sphereRadius = 1.0;
    float t;
    if (intersectSphere(ro, rd, sphereCenter, sphereRadius, t)) {
        vec3 hitPoint = ro + t * rd;
        vec3 normal = calculateNormal(hitPoint, sphereCenter);
        vec3 lightDir = normalize(vec3(-1.0, -1.0, -1.0));
        float diff = max(dot(normal, lightDir), 0.0);
        FragColor = vec4(diff, diff, diff, 1.0);
    } else {
        FragColor = vec4(0.0, 0.0, 0.0, 1.0);
    }
}
"""