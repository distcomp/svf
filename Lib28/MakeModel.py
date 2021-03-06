# -*- coding: UTF-8 -*-

from   sys    import *

from   GridVarArgs  import *
from   Pars   import *
from   Lego   import *
from   Parser import *
import COMMON as com
from   ModelFiles import *


def grids_add ( all_grids, from_ ) :    # пополняет из from_,  если уже нет в  all_grids
        for g in from_:                                           
            if findGridByName ( all_grids, g.name) == None :       # если еще нет 
                    all_grids.append(g)
        return all_grids 


def WriteGrid27 ( buf ):
            if buf == '': return
            Task = com.Task
            g = getGRID26(buf, Task.Grids)
            Task.AddGrid( g )
#            for ig, g in enumerate(Task.Grids):
            wr( '\n    '+g.name+ ' = ' + 'Task.Grids[' + str(len(Task.Grids)-1) + ']' )    #  g__p = Task.Grids[0]

            if g.className == 'Grid' :
                Swr(g.name+'=Grid(\''+g.name+'\','+str(g.min)+','+str(g.max)+','+str(g.step)
                                 +',\''+g.ind+'\',\''+g.oname+'\')')
            else :
                Swr(g.name+'=Domain (\''+g.name+'\','+g.A[0].name+','+str(g.visX))
                if g.dim==1: Swrs(')')
                else       : Swrs(','+g.A[1].name+','+str(g.visY)+')')
            Swr('Task.AddGrid('+g.name+')')


def WriteVarParam26 ( buf, param ) : #, testSet, teachSet ):
        if buf == '':  return
        if co.printL:  print ('VarParam26:', buf, param)
        Task = com.Task
 
        strInitBy = ''
        strFuncDomain = ''
        Lbound = None
        Ubound = None
        Finitialize = None #'1'
        AddGap = False
        fun = None

        parts = buf.split(';')
        p = -1                                              #  вставляем точку с зап
        if   parts[0].find('<') > 0 : p=parts[0].find('<')   #    X(t) <= 0
        elif parts[0].find('>') > 0 : p=parts[0].find('>')   #   X(t) >= 0
        elif parts[0].find('=') > 0 : p=parts[0].find('=')   # Param:  H(X,Y) = DEM_Kostica.asc
        elif parts[0].find('\\inn')>0: p=parts[0].find('\\inn')   # Param:  H(X,Y) \\in [0,1]
        if p > 0 :
            parts[0] = parts[0][:p] + ';' + parts[0][p:]
            print('P0', parts[0])
            buf1 = ';'.join (parts)
            parts = buf1.split(';')

        for i, part in enumerate (parts) :
                part = Task.substitudeDef ( part )
                part_blanck = part
                part = part.replace(' ','')
                if part == '' :   continue
                up_part = part.upper()
                pars = parser ( part )
                if co.printL:  print ('PART:', part)
                print('PART:', part, i)

                if i==0 :                                       #  Функция  X(t)
                    fun = Fun(pars.items[0].part ,pars.Args(1), param )

                elif part[0] == '=' :             # Param:  H(X,Y) = DEM_Kostica.asc
                            Finitialize = part[1:]
                elif getGRID26 ( pars, Task.Grids ) != None :   #  Грид
                        gr = co.LastGrid  # getGRID26 ( pars, Task.Grids )
#                        print ('gr.name',  gr.name, pars.myprint())
                        if co.printL:  print ('gr.name:', gr.name, gr.className)
                        if gr.name == '__No__Name__' : gr.name = fun.V.name
                        if gr.name == fun.V.name :              #  bounds     for x(t)    x ∈ [ -10.,10 ];
                            Lbound = gr.min
                            Ubound = gr.max
                            if co.printL:  print ('LG:', Lbound)                         #   Polynome  не проверено !!!!!!!!!!!!!!!!!!!!!!!!!!
                            if co.printL:  print ('UG:', Ubound)
                        else :
                            if gr.className == 'Domain' :    #  PHqt  ( Q, T );  Q,T ∈ QT;
                                fun.domain = gr
                                args = part.split('\\in')[0].split(',')
     #                           print (args)
                             #   1/0
                                for ia,a in enumerate(fun.A) :
                                    gri = Grid (findGridByName ( Task.Grids, gr.A[args.index(a)].name ))
                                    gri.name = a
                                    fun.A[ia] = gri
                                continue
                            for ia, a in enumerate(fun.A):
                                if co.printL:  print ('Arg:', a, type(a), type('abc'),)
                                if type(a) != type('abc') : continue
#                                print gr.name, a
                                if gr.name == a :
#                                    fun.A[ia] = Grid (gr)
                                    fun.A[ia] = (gr)
#                                    fun.A[ia] = Arg (gr)
                                    if co.printL: print ('ArgName:', fun.A[ia].name)
                                    break
                            else :
                                    print ('********  NO USE FOR ARG GRID ', gr.name, '*********************')
                                    exit(-1)

#                elif part.find('\\in')==0 :
 #                           p = max (part.find('>'), part.find('>=')+1)
  #                          Lbound = getfloat(part[p+1:])
   #                         if co.printL:  print ('Lbound=', Lbound)
                elif part.find('>') == 0:
                            p = max(part.find('>'), part.find('>=') + 1)
#                            Lbound = getfloat(part[p + 1:])
                            Lbound = part[p + 1:]
                            if co.printL:  print('Lbound=', Lbound)
                elif part.find('<')==0 :
                            p = max (part.find('<'), part.find('<=')+1)
#                            Ubound = getfloat(part[p+1:])
                            Ubound = part[p+1:]
                            if co.printL:  print ('Ubound=', Ubound)

                elif up_part.find('POLYPOW')==0 :
                            fun.maxP = int(part.split('=')[1])
                elif up_part.find('VARTYPE')==0 :
                            fun.type = part.split('=')[1]
                elif up_part.find('DATAFILE')>=0 :    co.ReadFrom = '* from '+ part.split('=')[1]
                elif up_part.find('SELECT')>=0 :      co.ReadFrom = part_blanck[8:]
#                elif up_part.find('INITIALIZE')>=0 :  Finitialize = part.split('=')[1]   # 22.12.19

#                elif part.find('\\in')>=0 :                                     #  не проверено и не понятно  ???????????????????
 #                           tmp = part.split('\\in')
  #                          if tmp[0].find(',')>=0 :  strFuncDomain = tmp[1]           # Function Domain для NDT
   #                         else :   all_grids.append ( readGrid19 ( part, '\\in' ) )
                            
                elif up_part.find('INITBY')>=0 :    #  для явного задания NDT   #  не проверено
                            strInitBy = up_part[6:]
                    
                elif part.find (fun.V.name) >=0:
                    parts[i] = 'EQ:' + part
                    if co.printL:  print ('treated as EQ:',  parts[i])
                elif up_part == 'ADDGAP' :
                    AddGap = True
                else :
                    print ('**************** Cant understand :', part)
                    exit (-1)

        if fun.dim == 1 and type(fun.A[0]) == type('abc') :        # Domain
 #           print ('11111111111111111', fun.A[0]);  1/0
            if not findGridByName ( Task.Grids,fun.A[0] ) is None:
#                print 'LL'
                gr = co.LastGrid
 #               print '2', gr.name
                if gr.className == 'Domain':  # PHqt  ( QT );
                    fun.domain = gr
                    fun.A[0] = Grid(gr.A[0])
                    fun.A.append (Grid(gr.A[1]))
                    fun.dim = 2

        f_name = fun.V.name
        Prefix_name = co.funPrefix + f_name
        dim = fun.dim

        f_str = 'Fun(\''+fun.V.name+'\',['        #    write  into the  StastModel
        if co.ReadFrom != '' :
            Swr ('co.ReadFrom = \'' + co.ReadFrom + '\'' )
        for ia, a in enumerate (fun.A) :
            if ia!=0 : f_str += ','
            if type(a) == type('abc'):
                if findGridByName ( Task.Grids,a ) is None: f_str += '\''+a+'\'' # в кавычках, чтобы создать грид
                else                                      : f_str += a
            else :
                f_str += 'Grid(\''+a.name+'\','+str(a.min)+','+str(a.max)+','+str(a.step)\
                               +',\''+a.ind+'\',\''+a.oname+'\')'
#                print ('Grid(\''+a.name+'\','+str(a.min)+','+str(a.max)+','+str(a.step)\
 #                              +',\''+a.ind+'\',\''+a.oname+'\')')
        f_str += '],' + str(fun.param)
        if fun.maxP < 0 :
            Swr (fun.V.name+' = '+f_str+'); ')
            if fun.type == 'G':  Swr (fun.V.name+'.type = \'G\'; ')
        else :
            Swr(fun.V.name + ' = pFun(' + f_str+ ',' + str(fun.maxP) +'))')
        if not fun.domain is None :
            Swr(fun.V.name + '.domain = ' + fun.domain.name )
#        Swr ('Task.InitializeAddFun ( '+fun.V.name+ ', \''+ Finitialize +'\' )')
        Swr ('Task.InitializeAddFun ( '+fun.V.name )
        if Finitialize is None : Swrs (' )')
        else :                   Swrs ( ', \''+ Finitialize +'\' )')
        Swr( fun.V.name + '__f = ' + fun.V.name)
        if AddGap :   Swr ( fun.V.name+'.AddGap( )')

        if   dim == 0  :  Swr( Prefix_name + ' = ' + f_name + '.grd')  #
        elif dim == 1:
            Swr('def ' + Prefix_name + '(' + getName(fun.A[0]) + ') : return '
                        + f_name + '.F([' + getName(fun.A[0]) + '])')  # def fE (t) : return E.F([t])
        elif dim == 2:
            Swr('def ' + co.funPrefix + f_name + '(' + getName(fun.A[0]) + ',' + getName(fun.A[1]) + ') : return '
                        + f_name + '.F([' + getName(fun.A[0]) + ',' + getName(fun.A[1]) + '])')


        if fun.maxP >=0 :
            fun = pFun(fun)

        if not com.Preproc:
            fun = fun.Initialize( Finitialize )

        co.ReadFrom = ''

#        if fun.maxP >=0 :
 #           fun = pFun(fun)

        Task.AddFun ( fun )
#        if co.printL:
        Task.Funs[-1].myprint()

        if not com.Preproc :
            if strInitBy != '' :
                        print ('strInitBy', readListFloat19 (strInitBy,'(',cut2=')' ) )
                        ar = readListFloat19 (strInitBy,'(',cut2=')' )
                        Task.Funs[-1].InitBy (ar[0],ar[1],ar[2])     # -1  !!!!!!!!!!!!!!!!!!!
            if strFuncDomain != '' :
                        print ( strFuncDomain, Task.getFunNum(strFuncDomain) )
                        Fdomain = Task.getFun(strFuncDomain)
                        for a0 in Fdomain.A[0].NodS :
                            for a1 in Fdomain.A[1].NodS :
                                co.Task.Funs[-1].neNDT[a0,a1] = Fdomain.grd[a0,a1]
                        co.Task.Funs[-1].calcNDTparam()
            if AddGap : co.Task.Funs[-1].AddGap()


#        if not com.MakeModel : return

        f = com.ModelFile
        f_num = len ( Task.Funs ) -1
        d = Task.Funs[f_num]
        f_str = 'Funs['+str(f_num)+ ']'
        if Finitialize is None  : Finitialize = '1'
#        f_name = d.V.name
        wr(' \t\t\t\t\t\t\t\t\t\t\t# '+buf )
        wr('    ' + f_name + ' = ' + f_str + ';  ' + f_name + '__f = ' + f_name )
        if  d.param :                                                 # Param
                      wr ( '    '+ f_name + '__i = ' + f_str+'.grd' )
#                      wr ( '    '+ f_name + '__i = ' + f_str+'.grd;  Gr.grd'+str(f_num)+' =  ' + f_name + '__i' )
        else :
            if d.maxP >= 0:   # Poly
                  wr ( '    ' + f_name + '__i = Var ( range (PolySize(' + str(d.dim)+','+str(d.maxP)+') ), initialize = 0 )' )
            else :            # Grid               
                  if not d.param :                                                 # Var
                      wr ( '    ' + f_name + '__i = Var ( ' )
                      for di in range (d.dim) :
                          wrs ( f_str+'.A['+str(di)+'].NodS,' )
#                          f.write(f_str + '.A[' + str(di) + '].NodS,')
                      wrs ( 'domain='+str(d.domain_)+',' )
#                      f.write( 'domain='+str(d.domain_)+',' )
                      if not (Lbound is None and Ubound is None):
                          wrs ( ' bounds=('+str(Lbound)+','+str(Ubound)+'),')
                      wrs ( ' initialize = '+Finitialize+' )' )
          #            f.write(' initialize = ' + Finitialize + ' )')
            wr ( '    '+f_name+'.grd = ' + f_name + '__i ; Gr.'+f_name+' =  ' + f_name + '__i' )
#            wr ( '    '+f_str+'.grd = ' + f_name + '__i ; Gr.grd'+str(f_num)+' =  ' + f_name + '__i' )
#            if not d.V.dat is None:
            if d.maxP < 0:   # Grid
                      wr( '    '+f_name+'.InitByData()' )
 #                     wr( '    Funs['+str(f_num)+'].InitByData()' )
 #       wr ( '    Gr.F.append( ' +f_name+' )' )                    #27
#        if not d.param :
        if not d.neNDT is None:                     #27
            wr( '    '+f_name+'.Fix()' )
        if   dim == 0  :  wr('    ' + Prefix_name + ' = ' + f_name + '__i')  # =  __i
        elif dim == 1:
            wr('    def ' + Prefix_name + '(' + getName(fun.A[0]) + ') : return '
                        + f_name + '__f.F([' + getName(fun.A[0]) + '])')  # def fE (t) : return E.F([t])
        elif dim == 2:
            wr('    def ' + co.funPrefix + f_name + '(' + getName(fun.A[0]) + ',' + getName(fun.A[1]) + ') : return '
                        + f_name + '.F([' + getName(fun.A[0]) + ',' + getName(fun.A[1]) + '])')
        if d.maxP >= 0 and not d.param:   # Poly
            wr ( '    ' + f_name + '__i[0].value = ' + Finitialize )
# EQ:
        if d.maxP >= 0:   # Poly
            if not Lbound is None :
                WriteModelEQ26 ( parts[0] + '>=' + str(Lbound)  )
            if not Ubound is None :
                WriteModelEQ26 ( parts[0] + '<=' + str(Ubound)  )
                
        for part in parts :
#            print 'P:', part
            if part.find('EQ:') == 0:    WriteModelEQ26 ( part[3:] )


def fromTEX(equation) :
#    equation = UTF8replace(equation, '\\cdot', '*')
 #   equation = UTF8replace(equation, '\\limits', '')
  #  equation = UTF8replace(equation, '\\left',   '')
   # equation = UTF8replace(equation, '\\right',  '')
    print ('TEXsubst', equation)

    sel = parser(equation)
    repars = True
    while (repars) :
        repars = False
        for itn, it in enumerate(sel.items) :
            if it.type == 'name' or it.type == 'fun' :
                if it.part == '\\frac' :                    #  \frac{d}{dro}(Df) = Pdf
                    repars = True
                    it.part = ''
                    sel.items[itn+1].part = ''
                    pos = sel.items[itn+1].etc[1]
                    sel.items[pos].part = '/'
                    pos += 1
                    sel.items[pos].part = ''
                    pos = sel.items[pos].etc[1]
                    sel.items[pos].part = ''
                    pos += 1
                    if sel.items[pos].part == '{' :   #  замена  {}  ()
                        sel.items[pos].part = '('
                        pos = sel.items[pos].etc[1]
                        sel.items[pos].part = ')'
                if it.part.find ('\\int_') == 0 :        # INTEGRAL  запись  ∫_{0}^{rp}{d(x)*expr} -> ∫(0,rp,d(x)*expr)
                    repars = True
                    it.type = 'int'
                    lim_min = it.part.split('_')[1]
                    print ('lim_min', lim_min)
#                    UTF8replace (it.part,'\\int_','\\int(')
   #                 print (it.part)
                    it.part=it.part[0:4]+'('+lim_min
  #                  print(it.part)
                    pos = itn+1
                    if len (lim_min) == 0 :                     # {lim_min}  in   int_{lim_min}
                        sel.items[itn+1].part = ''
                        sel.items[sel.items[itn+1].etc[1]].part = ''
                        pos = sel.items[itn+1].etc[1]+1
                    sel.items[pos].part = ','
                    pos += 1                                    # lim_max
                    if sel.items[pos].part == '{' :
                        sel.items[pos].part = ''
                        pos = sel.items[pos].etc[1]
                        sel.items[pos].part = ''
                    sel.items[pos].part += ','
                    pos += 1                                    # { body }
                    sel.items[pos].part = ''
                    pos = sel.items[pos].etc[1]
                    sel.items[pos].part = ')'
                if repars :
                    equation = sel.join()
                    sel = parser(equation)
                    print ('Tex', it.part, equation );  sel.myprint()
        if co.UseHomeforPower :
            equation = UTF8replace(equation, '^', '**')
        else :
            equation = UTF8replace(equation, '^', '')
        return equation

def ParseEQUATION ( equation, all_grids ) :
        Task = com.Task
        Funs = Task.Funs

#        print 'Beg:', equation
        dif_minus = []                               # DERIV     (H2O((t+1.0))-H2O(t))/1.0==-E(t)*2.0736+WF*WD(t)
        dif_plus = []                               # DERIV 2

        equation = fromTEX(equation)
        if not co.Preproc :
            equation = Task.substitudeDef (equation)

        eqPars   = parser ( equation )
                                           #  Добавляем опущенные Аргументы
        if co.printL:  print ('ParseEQUATION'); eqPars.myprint()
        reparse = True
        while reparse :
          reparse = False
          for iit, it in enumerate(eqPars.items) :
            if it.type == 'name' :                  # нет  (
                if iit < len(eqPars.items)-1 :
                    if eqPars.items[iit+1].part == '.' : continue          #  F.Complex...
                for f in Funs :
                    if f.V.name == it.part and len(f.A) > 0:
                        for ia,a in enumerate( f.A ) :
                            if ia == 0:  it.part += '('
                            else      :  it.part += ','
                            if type( f.A[ia] ) == type('abc') : it.part += f.A[ia]
                            else                              : it.part += f.A[ia].name
                        it.part += ')'
                        if co.printL:  print ('NewPart',  it.part)
                        reparse = True
          if reparse :  eqPars   = parser ( eqPars.join() )
        if co.printL:  eqPars.myprint()
        

                        
        for it in eqPars.items :
            if it.lev == 0 and  ( it.part[0] in [ '=', '<', '>' ] )  :     # '='  ->  '=='  '=-/ -> ==-
                if com.printL : it.myprint() 
                if   len (it.part) == 1 :                        it.part += '=' 
                elif len (it.part) == 2 and it.part[1] != '=' :  it.part  = it.part[0] + '=' + it.part[1:] #  '=-'  -> '==-'
                
                if com.printL : print ('AFTER') ;  it.myprint()

        for g in Task.Grids:                                       # пополняем  all_grids  из общих Гридов      
            if findGridByName ( all_grids, g.name) == None :       # если еще нет 
                if eqPars.find_part_type ( g.name, 'name' ) >= 0 : # пока ищем in name
                    all_grids.append(g)

#        print 'ALL_Grids', len(all_grids)
 #       for g in all_grids : print g.name 

#####??        eqPars = parser ( equation )
        eqPars.funs( all_grids )                                        #  ... name -> grid
        dif_minus, dif_plus  = eqPars.dif1 ( dif_minus, dif_plus, all_grids )
        dif_minus, dif_plus  = eqPars.dif2 ( dif_minus, dif_plus, all_grids )
        integral_grids = eqPars.integral( all_grids )                       # лучше оставить последним - там всякие for и sum
 #       for itn, it in enumerate( eqPars.items ) :
  #          if it.part == '.' and eqPars.items[itn-1].type == 'var'  :  it.part = '__p.'
        equation = eqPars.join()
        if com.printL : print ('END PARSE', equation)
        
#        print 'INTids', len(integral_grids)
 #       for g in integral_grids : print g.name 

        constraint_grids=[]                         #  фигурируют в EQ  но не как  d(t)
        for g in all_grids :
            if com.printL : print (g.name)
            if findGridByName ( integral_grids, g.name) == None :            #  
                constraint_grids.append(g)

  #      print 'con Grids', len(constraint_grids)
   #     for g in constraint_grids: print g.name
   
        return  equation, eqPars, constraint_grids, dif_minus, dif_plus

eqNUM = 0

def WriteModelEQ26 ( buf ):
#        if not com.MakeModel : return
        if buf == '' : return
        global eqNUM
        eqName = 'EQ'+str(eqNUM)
        if co.printL:  print (eqName)
        Task = com.Task

        b_if = ''                                   #  Constraint.Skip
#        print (buf,  buf[:2])
        if buf[:2] == 'if' :
            if_p = buf.split(':')
            if len(if_p) > 1 :
                b_if = 'if not (' + if_p[0][2:] + ') : '
                buf = ''.join(if_p[1:])


        parts = buf.split(';')                      #  ; отделяет Гриды and conditions
        parts = list(filter(('').__ne__, parts))    # удаляет пустые элементы ''
        if co.printL:  print (eqName, parts)
        
        equation = parts[0]                       #  первая часть !
        equation = equation.replace(' ','')
        
        all_grids = []                              #  local (заданные в EQ  после ; and global grids
#        b_if = ''                                   #  Constraint.Skip
        for part in parts[1: ] :
            if not co.Preproc : part = Task.substitudeDef ( part )
            gr = getGRID26 (part, Task.Grids)
            if not gr is None :  all_grids.append ( gr )
            else              :
                print ('Can\'t treat  |' +part+ '|  in  '+buf)
                exit(-1)


        equation, eqPars, constraint_grids, dif_minus, dif_plus = ParseEQUATION ( equation, all_grids )

        for g in constraint_grids:
            eqPars.substAllNames (g.name, g.ind)
            eqPars.substAllNames (g.name+'__p', g.name)
        for fu in Task.Funs:
            eqPars.substAllNames(fu.V.name, co.funPrefix+fu.V.name)

        equation = eqPars.join()
        if com.printL : print ('EQAFTER', equation)

        f = com.ModelFile                            #   WRITE
        wr(' \t\t\t\t\t\t\t\t\t\t\t# '+buf )
        wr ( '    def '+eqName+' (Gr' )                   # def EQ*(Gr,t) :
        for g in constraint_grids :
            wrs ( ','+g.ind )
        wrs ( ') :' )
#        if b_if != '' :  wr('        if not ('+b_if+') : return Constraint.Skip')         #  Constraint.Skip
        if b_if != '' :  wr('        ' + b_if + 'return Constraint.Skip')         #  Constraint.Skip
        wr('        return (')
        wr('          '+equation)
        wr('        )')
        wr('    Gr.con'+eqName+' = Constraint(')                                  
        for ng, g in enumerate(constraint_grids) : 
            if co.printL:  g.Gprint()
            my_range = 'FlNodS'
            if g.name in dif_plus:  my_range  = 'm' + my_range
            if g.name in dif_minus: my_range  = my_range + 'm'
#            wrs ( g.name + '__p.' + my_range + ',')
            wrs(g.name + '.' + my_range + ',')
#            wrs('myrange('+str(g.min) )
 #           if g.name in dif_plus:   f.write ('+'+str(g.step)+','+str(g.max))           # myrange(0+1,179),
  #          else :                   f.write (','+str(g.max))                           # myrange(0,179),
   #         if g.name in dif_minus:  f.write ('-'+str(g.step)+','+str(g.step)+'),')     # myrange(0,179-1),
    #        else :                   f.write (','+str(g.step)+'),')                     # myrange(0,179),
        wrs('rule='+eqName+' )')                                                    # rule=DifEQ )

        eqNUM += 1
        return

def WriteModelDef26 ( code ):                       #   DEF:
#        if not com.MakeModel : return
        if code == '' : return
#        code = com.Task.substitudeDef (code)

        code, eqPars, constraint_grids, dif_minus, dif_plus = ParseEQUATION ( code, com.Task.Grids )
        
        parts = code.split('==')
        wr ( '    def '+parts[0]+': return '+parts[1]+'\n' )    # Code  for r in T.A[0].NodS:  T.gap[r,21]=0

def WriteModelCode26 ( code ):                      #   CODE:
        if code == '':  return
#        if not com.MakeModel : return
        code = com.Task.substitudeDef (code)
#        wr ( '    '+code+'\n')                               # Code  for r in T.A[0].NodS:  T.gap[r,21]=0
        wr ( '    '+code)                                 # Code  for r in T.A[0].NodS:  T.gap[r,21]=0


def WriteModelOBJ19 ( Q, obj ):                        #   OBJ:
#        if not com.MakeModel : return
        Task = com.Task
        Funs = Task.Funs
        f = com.ModelFile
        MsdType = ''
        Delta_Formula = 'Gr.F[fNum].Ftbl(n)-tbl[n]'  #  ПРОВЕРИТЬ  !!!!  заменить   Gr.F ->  Task.Funs

        obj, eqPars, constraint_grids, dif_minus, dif_plus = ParseEQUATION ( obj, [] )

        for fu in Task.Funs:
            eqPars.substAllNames_but_dot(fu.V.name, co.funPrefix + fu.V.name)

        eqPars.substAllNames_but_dot('Compl', 'Complexity')

        obj = eqPars.join()

        beg = 0
        while obj.find('.Complexity(',beg) >=0 :                        #  (..)  -> ([..])
            beg = obj.find('.Complexity',beg)+len('.Complexity')
            if obj[beg+1] == '[' : continue
            begi, in_br, end = getFromBrackets ( obj, '(', beg )
            obj = begi + '([' + in_br + '])' + end
        if co.printL:  print ('OBJ:', obj)
        beg = 0
        while obj.find('.ComplCycle(',beg) >=0 :                        #  (..)  -> ([..])
            beg = obj.find('.ComplCycle',beg)+len('.ComplCycle')
            if obj[beg+1] == '[' : continue
            begi, in_br, end = getFromBrackets ( obj, '(', beg )
            obj = begi + '([' + in_br + '])' + end
        beg = 0
        while obj.find('.ComplCyc0E(',beg) >=0 :                        #  (..)  -> ([..])
            beg = obj.find('.ComplCyc0E',beg)+len('.ComplCyc0E')
            if obj[beg+1] == '[' : continue
            begi, in_br, end = getFromBrackets ( obj, '(', beg )
            obj = begi + '([' + in_br + '])' + end
        if co.printL:  print ('OBJ:', obj)

        obj, eqPars, constraint_grids, dif_minus, dif_plus = ParseEQUATION ( obj, [] )


        com.lenPenalty = 0
        for itn, it in enumerate (eqPars.items) :
            if it.part == 'Penal' :
                com.lenPenalty = max (com.lenPenalty, int(eqPars.items[itn+2].part)+1 )

 #       if not com.MakeModel : return


        if obj == 'N' :
          obj = ''
          penNum = 0
          for fu in Funs :
            if fu.param : continue
            if len(fu.A) == 0 : continue
            if len(obj) > 0 :  obj += '+'
            obj += fu.V.name + '.Complexity(['
            for a in fu.A :
                if a != fu.A[0] : obj += ','
                obj += 'Penal[' + str(penNum) + ']'
                penNum += 1
            obj += '])/' + fu.V.name + '.V.sigma2'
            obj += ' + ' + fu.V.name + '.MSDnan()'
            com.lenPenalty = penNum
        else :
          objP = obj.split('defMSD')
          if len(objP) == 2 :  #>1
            p_plus = objP[0].rfind('+')
            if p_plus <= 0 : p_plus = 0
            fNum = com.Task.getFunNum(objP[0][p_plus+1:-1])
#            print objP
            beg, delta, end = getFromBrackets (objP[1],'(')
            if beg == None :  beg, delta, end = getFromBrackets (objP[1],'{')  #  стары1 вариант
            MsdType = beg
            print ('MsdType=', beg, delta, end)
  #          print 'DELTA1', delta
            if delta !='' and delta !=' ' :
                for ifu, fu in enumerate ( com.Task.Funs ) :
                    pf = delta.find (fu.V.name)
                    if pf>=0 : delta = delta.replace(fu.V.name, 'Gr.F['+str(ifu)+'].Ftbl(n)' )  # replace   f for  Gr.F[...
#                print 'DELTA2', delta
                Delta_Formula = delta
            if co.printL:  print (delta)
            obj = objP[0][:p_plus+1] + 'defMSD(Gr,'+str(fNum)+')'+end
            if co.printL:  print (obj)
#       Penalty
        if len (com.Penalty) == 0 :
#            print '********C', obj.count('Penal[')
            for p in range(obj.count('Penal[')) : com.Penalty.append (.1)

        for itn, it in enumerate(eqPars.items):
            if it.part == 'MSD' or it.part == 'MSDnan' : # or it.part == 'MSDcheck'
                fn = (eqPars.items[itn-2].part)
                wr('\n    ' + fn + '.mu = Gr.mu;')
                wrs(' ' + fn + '.testSet = co.testSet;')
                wrs(' ' + fn + '.teachSet = co.teachSet')

        wr(' \t\t\t\t\t\t\t\t\t\t\t# ' + obj)
        wr('    def obj_expression(Gr):  \n        return (')
        wr('             ' + obj )                             #   Gr.F[1].Complexity ( [Penal[0]] ) + Gr.F[0].MSD()
        wr('        )  \n    Gr.OBJ = Objective(rule=obj_expression)  \n')
        f.write('\n    return Gr\n')        # end of    createGr ( Task, Penal ) :

        if False :    ########################################  Пока убрали
          wr ( 'def Delta (Gr, fNum, tbl, n) : ')
          if MsdType=='noTbl' or MsdType=='':
            wr ( '    return  '  + Delta_Formula )
          else :
            wr ( '    return  '  + Delta_Formula + '- tbl[n]' )
          wr ( 'def DeltaVal (Gr, fNum, tbl, n) :')
          if MsdType=='noTbl' or MsdType=='':
            wr ( '    return  (' + Delta_Formula + ')()' )
          else :
            wr ( '    return  (' + Delta_Formula + ')()- tbl[n]' )
#            wr ( '    return  Gr.F[fNum].tbl[n,Gr.F[fNum].V.num] - ('+Delta_Formula+')()' ) #   Gr.F[fNum].Ftbl( n )() ')

          wr ( 'def defMSD ( Gr, fNum ) :')
          wr ( '            ret = 0')
          wr ( '            num = 0')
          wr ( '            s = Gr.F[fNum]')
          wr ( '            for n in s.sR :')
          if MsdType!='noTbl' :
            wr ( '                if not isnan(s.V.dat[n])  : ')
          wr ( '                      ret += s.mu[n] * Delta (Gr, fNum, s.V.dat, n) **2')
          wr ( '                      num += s.mu[n]')
          if MsdType=='noTbl' :
            wr ( '            ret = 1./num * ret')
          else :
            wr ( '            ret = 1./s.V.sigma2 /num * ret')
          wr ( '            return ret')

          wr ( 'def defMSDVal ( Gr, fNum ) :')
          wr ( '            ret = 0')
          wr ( '            num = 0')
          wr ( '            s = Gr.F[fNum]')
          wr ( '            for n in s.sR :')
          if MsdType!='noTbl' :
            wr ( '                if not isnan(s.V.dat[n])  : ')
          wr ( '                      ret += s.mu[n]() * DeltaVal (Gr, fNum, s.V.dat, n) **2')
          wr ( '                      num += s.mu[n]()')
          if MsdType=='noTbl' :
            wr ( '            ret = 1./num * ret')
          else :
            wr ( '            ret = 1./s.V.sigma2 /num * ret')
          wr ( '            return ret')


 #                       Swr('Task.Delta     = Delta')
  #                      Swr('Task.DeltaVal  = DeltaVal')
   #                     Swr('Task.defMSD    = defMSD')
    #                    Swr('Task.defMSDVal = defMSDVal')



        f.write( '\ndef print_res(Task, Penal, f__f):\n' )                            #  print_res
        f.write( '\n    Gr = Task.Gr' )
        for nf, fu in enumerate( Task.Funs ) :
            if obj.find(fu.V.name) >= 0 :
                wr( '\n    '+fu.V.name+ ' = ' + 'Task.Funs[' + str(nf) + ']' )    #  f__p = Gr.F[1]
        f.write ( '\n\n    OBJ_ = Gr.OBJ ()' )
 #       f.write ( '\n    print  \'    OBJ =\', OBJ_' )
  #      f.write ( '\n    print >> f__f,  \'\\n    OBJ =\', OBJ_\n' )
        f.write('\n    print (  \'    OBJ =\', OBJ_ )')
        f.write('\n    f__f.write ( \'\\n    OBJ =\'+ str(OBJ_)+\'\\n\')\n')
#        obj_parts = obj.replace(' ', '').split('+')   ##############    ' '->'' !!!!!!!
 #       if len (obj_parts) > 1 :
  #        for p in obj_parts :                              #  OBJ по частям  by parts

        from_ = 0;  to_ = 0                                 #  OBJ по частям  by parts
        for itn, it in enumerate(eqPars.items) :
          if it.part == '+' and it.lev == 0 or itn == len(eqPars.items)-1 :     # + or last element
            if itn == 0 :                                               # певый +
              from_ = 1
              continue
            if it.part == '+' :  to_ = itn-1
            else              :  to_ = itn                              # last
            if from_ <= 1  and  to_ == itn : break                      # единственный элемент
            part = eqPars.join ( from_, to_+1 )
#            if p == ' ': continue     # если нет штрафа
            f.write( '    tmp = (' + part + ')()\n' )
            f.write( '    stmp = str(tmp)\n')
#            f.write( '    print       \'    \',int(tmp/OBJ_*1000)/10,\'\\t' + part + ' =\', tmp\n' )
 #           f.write( '    print >> f__f, \'    \',int(tmp/OBJ_*1000)/10,\'\\t' + part + ' =\', tmp\n' )
            f.write( '    print (      \'    \',int(tmp/OBJ_*1000)/10,\'\\t' + part + ' =\', stmp )\n' )
            f.write( '    f__f.write ( \'    \'+str(int(tmp/OBJ_*1000)/10)+\'\\t' + part + ' =\'+ stmp+\'\\n\')\n' )
#            f.write( '    print       \'    \',int(tmp/Gr.OBJ()*1000)/10,\'\\t' + p + ' =\', tmp\n' )
 #           f.write( '    print >> f, \'    \',int(tmp/Gr.OBJ()*1000)/10,\'\\t' + p + ' =\', tmp\n' )
            from_ = to_ + 2
        f.write( '\n    return\n' )
        print ('Model was built')
        if  Q.upper() == 'OBJ:' :
#            com.ModelFile.close()
 #           com.ModelFile = 1    #  >> Null
            WrStart27()


def WrStart27 () :
    com.ModelFile.close()
    com.ModelFile = 1  # >> Null

    with open('Model.py', 'r') as mf:
        lines = mf.readlines()
        for nl, l in enumerate(lines):
            if nl > 0: Swrs(l)
    Swr('\ncom.Task.createGr  = createGr')
    Swr('\ncom.Task.print_res = print_res')
    Swr('\nco.lenPenalty = ' + str(co.lenPenalty))
    Swr('\nfrom SvFstart62 import SvFstart19')
    Swr('\nSvFstart19 ( Task )')  # 27   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def WriteModelOBJ_U (buf) :
        wr ('\ndef OBJ_U (Task):\n')
        for fu in range ( len( com.Task.Funs ) ) :
            wr( '    '+com.Task.Funs[fu].V.name+ ' = ' + 'Task.Funs[' + str(fu) + ']' )    #  f__p = Gr.F[1]
        wr ('    return '+buf)
        wr ('com.Task.OBJ_U = OBJ_U')
#        com.ModelFile.close()
 #       com.ModelFile = 1  # >> Null
        WrStart27()



