#version 330 core

// Variable de sortie (sera utilisé comme couleur)
out vec4 color;

uniform vec4 color1;

//Un Fragment Shader minimaliste
void main (void)
{
  //Couleur du fragment
  color = color1;

  }
