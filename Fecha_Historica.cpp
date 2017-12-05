#include <iostream>
//#include <cstdlib>
#include <sstream>
#include <set>
#include "/usr/include/c++/5/bits/stl_pair.h"
#include "Fecha_Historica.h"
//#include <stdlib.h>
#include<string>
using namespace std;

iterator Fecha_Historica::begin(){  
  return events.second.begin();
}
const_iterator Fecha_Historica::begin()const{  
  return events.second.begin();
}
iterator Fecha_Historica::end(){  
  return events.second.end();
}
const_iterator Fecha_Historica::end()const{  
  return events.second.end();
}
//Constructor de copias
   Fecha_Historica::Fecha_Historica(const Fecha_Historica & e){
      events=e.events;
  
   }

   Fecha_Historica(int a, string *s, int n){
      set_year(a);
      for(int i=0;i<n;i++){
        add_event(s[i]);
      }

   }

  void Fecha_Historica::set_year(int a){
    events.first=a;
  }
//Añade un evento
  void Fecha_Historica::add_event(string& event){
      events.second.insert(event);
  }


//Buscador de eventos
  bool Fecha_Historica::search_event(string s, Fecha_Historica &matches){
      if(!matches.events.second.empty()){
        matches.events.second.clear();
      }

      bool encontrado=false;
     
      //defino it
      for(it=events.second.begin();it!=events.second.end();it++){
        if((*it).find(s)!=-1){
          matches.add_event(*it);
          encontrado=true
        }
      }

      if (encontrado){
        matches.set_year(get_year());
      }

      return encontrado; 
}

   //Operator =
   Fecha_Historica & Fecha_Historica::operator=(const Fecha_Historica & orig){
   events=orig.events;
    return *this;
  }

  //  Operador []
  string& Fecha_Historica::operator[](int i){
    assert(0<=i && i<get_size());
    const_iterator it=begin();
    advance(it,n);
    return *it;
  }
// Operador [] constante
  const string& Fecha_Historica::operator[](int i) const{
    assert(0<=i && i<get_size());
    const_iterator it=begin();
    advance(it,n);
    return *it;
  }
  


//Operador <<
  ostream& operator<< (ostream& os, const Fecha_Historica& e){
    os << e.get_year();
    fecha_Historica::const_iterator it;
    for(it=e.begin();it!=e.end();it++){
        os << '#' << (*it);
    }
      os << '\n';
    return os;
  }

//Operador >>
istream& operator>> (istream& is, Fecha_Historica& e){  
  string linea; 
  const char ALM='#';
  
  if(!e.events.second.empty()){
    e.events.second.clear();
  }
  
  getline(is,linea,ALM);
  e.events.first=atoi(linea.c_str());
  getline(is,linea);
  
  stringstream ss(linea);
  
  while(!ss.eof()){
    getline(ss,linea,ALM);
    e.add_event(linea);
  }
  return is; 
}  

 
