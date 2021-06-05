#version 330 core

in vec2 TexCoord;
in vec3 Normal;
in vec4 Vertex;

out vec4 FragColor;

//vec3 albedoV = vec3(1, 1, 1);
//float metallicV = 0.8;
//float roughnessV = 1;
float ao = 1;

uniform struct{
	vec4 baseColor;
	float roughness;
	float metallic;
} p3d_Material;

uniform struct p3d_LightSourceParameters {
    vec4 color;
    vec4 position;
    mat4 shadowViewMatrix;

    sampler2DShadow shadowMap;
} p3d_LightSource[8];

uniform struct p3d_FogParameters {
	vec4 color;
	float density;
	float start;
	float end;
} p3d_Fog;

uniform sampler2D p3d_Texture0;
uniform sampler2D p3d_Texture1;
uniform sampler2D p3d_Texture2;

const float PI = 3.14159265359;
// ----------------------------------------------------------------------------
float DistributionGGX(vec3 N, vec3 H, float roughness)
{
    float a = roughness*roughness;
    float a2 = a*a;
    float NdotH = clamp(dot(N, H), 0.0, 1.0);
    float NdotH2 = NdotH*NdotH;

    float nom   = a2;
    float denom = (NdotH2 * (a2 - 1.0) + 1.0);
    denom = PI * denom * denom;

    return nom /denom; // prevent divide by zero for roughness=0.0 and NdotH=1.0
}
// ----------------------------------------------------------------------------
float GeometrySchlickGGX(float NdotV, float roughness)
{
    float r = (roughness + 1.0);
    float k = (r*r) / 8.0;

    float nom   = NdotV;
    float denom = NdotV * (1.0 - k) + k;

    return nom / max(denom, 0.001);
}
// ----------------------------------------------------------------------------
float GeometrySmith(vec3 N, vec3 V, vec3 L, float roughness)
{
    float NdotV = max(dot(N, V), 0.0);
    float NdotL = max(dot(N, L), 0.0);
    float ggx2 = GeometrySchlickGGX(NdotV, roughness);
    float ggx1 = GeometrySchlickGGX(NdotL, roughness);

    return ggx1 * ggx2;
}
// ----------------------------------------------------------------------------
vec3 fresnelSchlick(float cosTheta, vec3 F0)
{
    return max(F0 + (1.0 - F0) * pow(1.0 - cosTheta, 5.0), 0.0);
}
// ----------------------------------------------------------------------------
void main()
{		
	vec3 albedo = pow(p3d_Material.baseColor.rgb * texture(p3d_Texture0, TexCoord).rgb, vec3(2.2));
	float metallic = p3d_Material.metallic * texture(p3d_Texture2, TexCoord).r;
	float roughness = p3d_Material.roughness * texture(p3d_Texture1, TexCoord).r;

    vec3 N = normalize(Normal);
    vec3 V = normalize(-Vertex.xyz);

    // calculate reflectance at normal incidence; if dia-electric (like plastic) use F0 
    // of 0.04 and if it's a metal, use the albedo color as F0 (metallic workflow)    
    vec3 F0 = vec3(0.04); 
    F0 = mix(F0, albedo, metallic);

    // reflectance equation
    vec3 Lo = vec3(0.0);
	float shadow;
	
    for(int i = 0; i < p3d_LightSource.length(); ++i) 
    {
		
		vec3 L;
		float attenuation;
		if(p3d_LightSource[i].position.w == 0.0){
			//It is a directional light
			L = p3d_LightSource[i].position.xyz;
			attenuation = 1.0;
			
		}
		else {
			// It is a point light
			L = p3d_LightSource[i].position.xyz - Vertex.xyz; 
			float distance = length(L);
			attenuation = 1 / (distance * distance);
		}
		vec3 radiance = p3d_LightSource[i].color.rgb * attenuation;
		L = normalize(L);
		vec3 H = normalize(V + L);

        // Cook-Torrance BRDF
        float NDF = DistributionGGX(N, H, roughness);   
        float G   = GeometrySmith(N, V, L, roughness);      
        vec3 F    = fresnelSchlick(clamp(dot(H, V), 0.0, 1.0), F0);
           
        vec3 nominator    = NDF * G * F; 
        float denominator = 4 * max(dot(N, V), 0.0) * max(dot(N, L), 0.0);
        vec3 specular = nominator / max(denominator, 0.001); // prevent divide by zero for NdotV=0.0 or NdotL=0.0
        
        // kS is equal to Fresnel
        vec3 kS = F;
        // for energy conservation, the diffuse and specular light can't
        // be above 1.0 (unless the surface emits light); to preserve this
        // relationship the diffuse component (kD) should equal 1.0 - kS.
        vec3 kD = vec3(1.0) - kS;
        // multiply kD by the inverse metalness such that only non-metals 
        // have diffuse lighting, or a linear blend if partly metal (pure metals
        // have no diffuse light).
        kD *= 1.0 - metallic;	  
		
        // scale light by NdotL
        float NdotL = max(dot(N, L), 0.0);

		

		// shadows
		shadow = textureProj(
				p3d_LightSource[i].shadowMap, p3d_LightSource[i].shadowViewMatrix * Vertex
			);

        // add to outgoing radiance Lo
        Lo += (kD * albedo / PI + specular) * radiance * NdotL * shadow;  // note that we already multiplied the BRDF by the Fresnel (kS) so we won't multiply by kS again
    }   
    
    // ambient lighting (note that the next IBL tutorial will replace 
    // this ambient lighting with environment lighting).
    vec3 ambient = vec3(0.02) * albedo * ao;

    vec3 color = ambient + Lo;

    // HDR tonemapping
    color = color / (color + vec3(1.0));
    //gamma correct
    color = pow(color, vec3(1.0/2.2));

	// fog
	float dist = distance(Vertex, vec4(0, 0, 0, 1));
	float fogFactor = 1.0 / exp((dist * p3d_Fog.density) * (dist * p3d_Fog.density));
	fogFactor = clamp(fogFactor, 0.0, 1.0);	

	vec4 finalColor = mix(vec4(color, 1.0), p3d_Fog.color, 1 - fogFactor);
	FragColor = finalColor;
}