#version 330 core

// Variable d'entrée, ici la position
layout (location = 0) in vec3 position;

uniform vec4 translation;
uniform vec4 rotation 

//Un Vertex Shader minimaliste
void main (void)
{
  //Coordonnees du sommet
  gl_Position = rotation * vec4(position,1.0);
  gl_Position += translation;
}

