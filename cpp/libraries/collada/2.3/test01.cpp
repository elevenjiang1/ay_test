#include <dae.h>
#define COLLADA_DOM_USING_141
#include <1.4/dom/domCOLLADA.h>
#include <dae/daeErrorHandler.h>
// #include <dae/daeTinyXMLPlugin.h>
// #define ColladaDOM ColladaDOM141
#include <iostream>
using namespace std;

int main(int argc,char**argv)
{
  // daeTinyXMLPlugin *tinyxmlio= new daeTinyXMLPlugin();
  const char *fname="box.dae";
  if(argc>1)  fname=argv[1];
  DAE *dae= new DAE;
  domCOLLADA *collada(NULL);
  collada = dae->open(fname);
  if (collada==NULL)
  {
    std::cerr<<"failed to open: "<<fname<<std::endl;
    return 1;
  }
  else
  {
    std::cerr<<"opened: "<<fname<<std::endl;
  }
  return 0;
}
