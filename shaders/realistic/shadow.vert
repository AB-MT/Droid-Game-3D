#version 330 core

uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;
uniform mat3 p3d_NormalMatrix;

in vec4 p3d_Vertex;
in vec3 p3d_Normal;
in vec2 p3d_MultiTexCoord0;

out vec2 TexCoord;
out vec3 Normal;
out vec4 Vertex;

void main() {
	Vertex = p3d_ModelViewMatrix * p3d_Vertex;
	gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
	TexCoord = p3d_MultiTexCoord0;
	Normal = p3d_NormalMatrix/*mat3(p3d_ModelMatrix)*/ * p3d_Normal;
}