<div align="center" class = "all" >
  <h1>
      Relatório do problema 1: Vende-Pass: Venda de Passagens
  </h1>

  <h3>
    Mailson Alves Silva Santos<sup>1</sup>, Matheus Mota Santos<sup>2</sup>
  
  </h3>
 

  <p>
    Engenharia de Computação – Universidade Estadual de Feira de Santana (UEFS)
    Av. Transnordestina, s/n, Novo Horizonte
    Feira de Santana – BA, Brasil – 44036-900
  </p>

  <center>mailsonalves.new@gmail.com<sup>1</sup></center>
  <center>matheuzwork@gmail.com<sup>2</sup></center>

</div>

# 1. Introdução

O crescimento da malha aérea brasileira nos últimos anos é justificado pelo aumento da demanda por voos domésticos e voos regionais no país. Ao tornar o transporte aéreo mais acessível para um público mais amplo, as companhias aéreas podem enfrentar, contudo, o problema da ineficiência logística e operacional.
Esse problema pode trazer grande prejuízo financeiro e atrapalhar o planejamento de alocação por demanda das companhias aéreas para algumas regiões.

Para solucionar esse problema, foi desenvolvido um sistema de redes para a compra de passagens aéreas, auxiliando as companhias na predição de demandas e alocação de recursos. Além disso, foi pensado na necessidade de prezar pela boa experiência do usuário/cliente que deseja comprar uma passagem aérea. O sistema foi implementado utilizando o conjunto de protocolos TCP/IP para fazer a comunicação entre as interfaces de clientes e o servidor da empresa aérea. 

Através de uma interface criada, um usuário do sistema pode consultar, comprar e cancelar passagens aéreas, tendo uma experiência simples e intuitiva. Além disso, o sistema desenvolvido é capaz de lidar com a concorrência de requisições, tratando os possíveis conflitos em casos de grande volume e disputa de recursos computacionais.

# 2. Referencial Teórico

As redes de computadores possibilitam a comunicação e o compartilhamento de dados entre diferentes dispositivos conectados, proporcionando o alicerce para sistemas distribuídos e o funcionamento da Internet. No contexto das redes modernas, o modelo TCP/IP (Transmission Control Protocol/Internet Protocol) é um dos principais pilares da comunicação em redes. Ele define um conjunto de protocolos que permite a troca de informações entre sistemas heterogêneos de maneira confiável e eficiente.
A camada de transporte do modelo TCP/IP é responsável por gerenciar a comunicação de dados entre dispositivos em uma rede, garantindo que as mensagens sejam entregues de forma confiável e ordenada. O socket é uma interface que facilita o uso da camada de transporte ao permitir que os desenvolvedores configurem e gerenciem conexões de rede de maneira programática. Por meio de sockets, é possível criar conexões, enviar e receber dados, e gerenciar o estado da comunicação, abstraindo a complexidade do processo e tornando a interação com a camada de transporte mais simples.

Para o desenvolvimento do sistema foi utilizado a linguagem de programação Python e algumas bibliotecas internas e recursos da linguagem como socket, threading e pickle. Para a criação de interfaces gráficas foi utilizado a biblioteca tkinter.

# 3. Metodologia

O sistema foi desenvolvido pensando em oferecer uma jornada de compra de passagem eficiente aos clientes de uma companhia aérea. A interface de usuário foi criada para ser simples e intuitiva. Os requisitos funcionais implementados foram:
- O usuário deve conseguir se cadastrar no sistema.
- O usuário deve conseguir fazer login no sistema.
- O usuário deve conseguir pesquisar por passagens aéreas inserindo o local de origem e destino.
- O usuário deve conseguir comprar uma passagem selecionada.
- O usuário deve conseguir cancelar uma passagem comprada por ele.

A estrutura do sistema é baseada na troca de mensagens entre um cliente da rede, que é um terminal que se conecta ao servidor, e o servidor, que é onde todas as informações sobre voos e clientes ficam registradas. A arquitetura do sistema é mostrada abaixo na Figura 1, que mostra os componentes da rede. Pode-se observar a centralidade do servidor e a troca simultânea de mensagens com vários clientes.
<p align="center">Figura 1. Modelo cliente servidor</p>
<div align="center">
<img src="https://github.com/user-attachments/assets/1b75e366-fb33-4d17-944d-69745d72f3b7" width="700">
</div>

Sendo assim, cada cliente da rede oferece uma interface de acesso que se comunica ao servidor e retorna para o usuário as informações solicitadas para o usuário do sistema. Essa comunicação entre cliente e servidor é detalhada na figura 2, que mostra um diagrama de sequência da troca de mensagens entre ambos no sistema.

Para o desenvolvimento do sistema foi implementado a comunicação entre cliente e servidor usando TCP/IP através do Socket. O Socket foi utilizado para facilitar o acesso à camada de transporte do TCP/IP realizando a comunicação de dois pontos em uma rede de computadores, nesse caso, entre cliente e servidor. Inicialmente, foi testada a comunicação direta entre um servidor e um cliente, posteriormente, foram testados múltiplos acessos simultâneos ao servidor. Após os testes, percebeu-se a necessidade de gerenciar a concorrência de acessos ao servidor, e para isso foi necessário a utilização de Threads. As Threads foram usadas para que vários clientes se comuniquem com servidor simultaneamente, deixando o servidor sempre em “escuta” de clientes que possam se conectar e fazer requisições para ele através da porta de rede especificada. Para gerenciar as Threads e evitar o uso demasiado de recursos computacionais com a criação de n Threads para n clientes, foi utilizado o pool de Threads para gerenciá-las.  O pool de threads permite processar várias requisições ao mesmo tempo, atribuindo uma Thread disponível do pool para cada requisição do cliente ao servidor. 

A arquitetura de software utilizada foi o padrão MVC(Model View Controller) visando organizar as classes de acesso aos dados, as interfaces e as classes intermediárias. Para os dados de voos e usuários do sistema foi criado uma função que serializa os dados utilizando a biblitoeca pickle em um arquivo do tipo JSON e fica disponível no servidor. Ao serem enviados em bytes via Socket, são desserializados e consumidos pelos clientes da rede. Ao sofrer alteração, como no momento de registro de compra de passagem, por exemplo, os dados são enviados e serializados novamente no servidor, ficando disponível para o demais clientes.
 
Para cada operação de cliente no servidor foi criado uma convenção de código, onde, na troca de mensagem é passado junto com um dado. Esse código leva a informação para uma função que faz uma operação específica no servidor. Dessa forma, foi criada uma API básica no servidor permitindo que o mesmo lide com as requisições específicas dos clientes da rede.
A Tabela 1 abaixo mostra os códigos e suas respectivas operações.

Tabela 1. Funções usadas no servidor e seus respectivos códigos



Uma função para teste de concorrência também foi implementada. 

# 4. Resultados 
Fica evidente que o sistema desenvolvido atendeu aos requisitos especificados, conseguindo lidar com o tráfego e concorrência durante a compra de passagens em diversos terminais simultâneos. Foi testado a compra para o mesmo assento do voo por mais de um cliente, e como esperado, o sistema tratou o erro da falta de vaga retornando corretamente a informação para os demais clientes da rede. Ademais, a experiência de compra do usuário atendeu aos requisitos e pode ser implementada para qualquer empresa aérea.
 
O sistema de venda de passagens aéreas Vende-Pass foi desenvolvido com a proposta de solucionar o problema da possível ineficiência logística e operacional das empresas aéreas brasileiras, além de oferecer uma jornada de compra de passagens satisfatória para os seus clientes. Estes objetivos propostos se tornaram viáveis graças ao uso de tecnologias de rede como o Socket, utilizados durante o seu desenvolvimento. Além disso, a utilização de recursos e arquiteturas de software usando a linguagem de programação Python também foram cruciais para resolução do problema.

# 5. Conclusão

Portanto, é possível concluir que após desenvolvido e testado, o sistema Vende-Pass atende a todos os requisitos aos quais lhe foram propostos, carecendo apenas de algumas melhorias como implementações de consulta rápida de passagens e voos disponíveis.

O aprendizado adquirido durante o processo de desenvolvimento do sistema abrange desde a área de redes de computadores até a Engenharia de Software e é fundamental para a formação dos discentes envolvidos.

# 6. Referências
