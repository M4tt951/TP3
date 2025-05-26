#version 330 core

// Variable de sortie (sera utilisé comme couleur)
out vec4 color;
in vec3 coordonnee_3d;

#uniform vec4 color1;

//Un Fragment Shader minimaliste
void main (void)
{
  //Couleur du fragment
  color = vec4(coordonnee_3d, 1.0);

  }