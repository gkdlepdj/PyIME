#-*- coding: cp949 -*-   
import msvcrt
# ����� �α׿�
import logging
from win32api import GetKeyState
from win32con import  VK_NUMLOCK
LOG_FILENAME = 'pyime.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)


# Ű���� ���� �ҹ��� -> �ѱ��ڸ� ���� 
lower_to_jm = [ 
u"��",u"��",u"��", u"��",u"��", u"��", u"��", u"��", u"��", u"��", 
u"��", u"��", u"��", u"��",  u"��", u"��", u"��", u"��", u"��", u"��", 
u"��", u"��", u"��", u"��", u"��", u"��"]
# Ű���� ���� �빮�� -> �ѱ��ڸ� ����
upper_to_jm = [ 
u"��",u"��", u"��", u"��", u"��", u"��", u"��", u"��",u"��", u"��",
u"K" ,u"��" ,u"��" ,u"��" ,u"��" ,u"��", u"��", u"��",u"��", u"��", 
u"��" ,u"��" ,u"��" ,u"��" ,"��" ,"��" ]

# �ʼ�,�߼�,���� �ε��� ����
CHO_DATA = u"��������������������������������������";
JUNG_DATA = u"�������¤äĤŤƤǤȤɤʤˤ̤ͤΤϤФѤҤ�";
# ������ �� �պ�ĭ�� ������ ���� ������ ǥ��
JONG_DATA = u" ������������������������������������������������������";

# ���� utf-8����� ��ȣ�ϳ� Ŀ�ǵ�â�� �ѱ��� ���̰� �ϱ����� cp949�� ���ڵ� 
ENCODING = 'cp949' 
def isascii(u):
    logging.debug("isascii u:%s %d", u.encode(ENCODING) , ( 0 < ord(u) < 0xff ) )
    return ( 0 < ord(u) < 0xff )
    
def isprint(c):
    k = ord(c)
    return ( 0x20<= k <=0x40 ) or ( 0x7b <=k <= 0x7e ) or \
               ( 0x41 <= k <= 0x5a) or ( 0x61 <= k <= 0x7a ) 

def get_capslock_state():
    return  GetKeyState( VK_NUMLOCK ) == 1 
    
def is_jaum(u_jm):
    """Ű���忡�� �Էµ� �ڸ� �������� �Ǵ�
    
        �ҽ������� ������ �ڸ� ������� �ϱ⶧���� ������ �ƴϸ� ����
    
    @�Ķ����: u_jm: �����ڵ� �ڸ�
    @��ȯ: �����̸� ��, �����̸� ���� 
    """
    return u_jm in CHO_DATA
    
def engkey2kor(c):
    """����Ű ��ȯ
    
        �����1�� -> �ѱ��ڸ�� �����Ͽ� ��ȯ
        
    @�Ķ����: c: Ÿ���� ��Ʈ����, ��ȯ�ϰ��� �ϴ� ����
    @��ȯ: �����ڿ� �ش��ϴ� �ڸ�, ����ҹ��ڰ� �ƴϸ� None
    """
    if c.islower():
        return lower_to_jm[ord(c)-97]
    if c.isupper():
        return upper_to_jm[ord(c)-65]
    return None
       
def asm(cho,jung,jong):
    """�����ڵ� �˾Ƴ��� 
    
        ��/��/�������� �ش� ������ �����ڵ带 ����. 
        �����ڵ忡�� �ѱ� ��~���� 0xAC00~0xD7A3�� �����ȴ�. 
        �̴� C��� �迭 3���� �迭�� ǥ���Ҽ� �ִ�. 
            ��) unicode[19][21][28] �ʼ�19,�߼�21,����28 �迭�� ���۹����� AC00
        ���� �ʼ� �߼� ������ ��(�ε�����)�� �˸� �ش������ �����ڵ带 ���� �� �ִ�.
        
    @�Ķ����: cho: Ÿ���� �����ڵ�, �ʼ� �ڵ�
    @�Ķ����: jung: Ÿ���� �����ڵ�, �߼� �ڵ�
    @�Ķ����: jong: Ÿ���� �����ڵ�, ���� �ڵ�
    @��ȯ: ��+��+���� �ش��ϴ� ������ �����ڵ� 
    """
    dcho = cho.encode(ENCODING) if cho else "*None"
    djung= jung.encode(ENCODING) if jung else "*None"
    djong = jong.encode(ENCODING) if jong else "*None" 
    if cho and not jung and not jong: return cho
    if not cho and jung : return jung    
    idx_cho  = CHO_DATA.find(cho)
    idx_jung = JUNG_DATA.find(jung)
    if jong:
        idx_jong = JONG_DATA.find(jong)
    else:
        idx_jong = 0    
    return unichr(idx_cho*21*28 + idx_jung*28 + idx_jong + 0xAC00)

def asm_jm(u_jm1,u_jm2):
    """��������/���߸��� �����ڵ� �˾Ƴ��� 
    
        �Է¹��� �� �ڸ� ���ļ� ���߸��� �Ǵ� ����������
        �����ڵ带 ��ȯ�Ѵ�
        
    @�Ķ����: u_jm1: Ÿ���� �����ڵ�,ù��° �ڸ�
    @�Ķ����: u_jm2: Ÿ���� �����ڵ�,�ι�° �ڸ�
    @��ȯ: �����ڸ� �����ڵ� ��ȯ , �ش��ڸ� ������ None
    """
    if u_jm1==u"��" and u_jm2 == u"��": return u"��"
    if u_jm1==u"��" and u_jm2 == u"��": return u"��"
    if u_jm1==u"��" and u_jm2 == u"��": return u"��"
    if u_jm1==u"��" and u_jm2 == u"��": return u"��"
    if u_jm1==u"��" and u_jm2 == u"��": return u"��"
    if u_jm1==u"��" and u_jm2 == u"��": return u"��"
    if u_jm1==u"��" and u_jm2 == u"��": return u"��"
    if u_jm1==u"��" and u_jm2 == u"��": return u"��"
    if u_jm1==u"��" and u_jm2 == u"��": return u"��"
    if u_jm1==u"��" and u_jm2 == u"��": return u"��"
    if u_jm1==u"��" and u_jm2 == u"��": return u"��"
    if u_jm1==u"��" and u_jm2 == u"��": return u"��"
    if u_jm1==u"��" and u_jm2 == u"��": return u"��"
    if u_jm1==u"��" and u_jm2 == u"��": return u"��"
    if u_jm1==u"��" and u_jm2 == u"��": return u"��"
    if u_jm1==u"��" and u_jm2 == u"��": return u"��"
    if u_jm1==u"��" and u_jm2 == u"��": return u"��"
    return None

def ime_wprint( u_code , bs=0 ):
    """ȭ������Լ�  
    
        ����(1��)�� ȭ�鿡 ����Ѵ�.
        �ι�° ���ڴ� �齺���̽��� Ƚ���� �����Ѵ�
        ����Ʈ ���� 0���� �̴� ������ ��µǾ��� ���ڸ� 
        ������ �ʰڴٴ� ���̴�. gotoxy(x,y)�� ����� �� ���� ȯ���̱⶧���� 
        �齺���̽��� �̿��Ͽ� ���� ���ڸ� �����. 
        ���� ���ڸ� ����� �ֿ��� ������ �ѱ��ڸ� �����ϴ� ���ȿ�
        ����Ŀ���� ������ ���� �����̴�. 
        
    @�Ķ����: u_code: Ÿ���� �����ڵ�,����ϰ��� �ϴ� ����(1��)
    @�Ķ����: bs: Ÿ���� ����,�齺���̽� Ƚ�� 
               �� ���ڸ� ����� ���ؼ� 2ȸ�� �齺���̽��� �����ؾ� �Ѵ�. 
    """
    for i in range(bs):
        msvcrt.putwch( u"\b" )
    
    if u_code:
        msvcrt.putwch(u_code)
    
"""
state: ������ ������������

         (0)               : �ʱ����    
          |                 
         (1)               : �ʼ��Է� ����
          |
         (2) -> (3)        : �߼��Է� ���� / �߼� ���߸��� ����
          |
         (4) -> (5)        : �����Է� ���� / ���� �������� ����
"""
state = 0  
# ���� �������� ��/��/���� ����
cho = None
jung = None 
jong = None 
jung1 = None  # ���߸��� ù��° ����
jung2 = None  # ���߸��� �ι�° ���� 
jong1 = None  #�������� ù��° ����
jong2 = None  #�������� �ι�° ����
input_list=[]
if __name__=='__main__':
    print """   �ѿ�Ű ������ (������忡���� �Է�)
                �ѿ���ȯ ---> number Lock Key"""
    while True :
        c = msvcrt.getch()
        # �ѹ���ũ�� ���� �ɷ������� 
        # �ѱ��Է����� �Ǵ� 
        if not get_capslock_state() :
            jm = engkey2kor(c)
        else:
            #�����Է����� �Ǵ� 
            jm = None
        # �ѱ�Ű �۵��Ǹ� ������
        if ord(c) > 127:
            msvcrt.putch('\x07')
            continue
        # ����Ű �Է� ����     
        if c == '\r' :
            if state != 0 :
                input_list.append( asm(cho,jung,jong) )
            msvcrt.putch('\r')
            msvcrt.putch('\n')
            for uc in input_list:
                msvcrt.putwch(uc)
            msvcrt.putch('\r')
            msvcrt.putch('\n')
            input_list=[]
            state = 0 
            cho=None;jung=None;jong=None
            continue
        # �齺���̽� �Է¹��� 
        if c == '\b' :
            if state==0 :
                # �������� ����
                # ����0
                try :
                    last_u = input_list.pop()
                except IndexError as e :
                    last_u = None
                if last_u :
                    if isascii(last_u):
                        ime_wprint(u' ',1)
                        msvcrt.putwch( u"\b" )
                    else:
                        ime_wprint(u' ',2)   
                        msvcrt.putwch( u"\b" )
            elif state==1:
                # �� �ʱ�ȭ
                # ����0
                state=0
                cho=None
                msvcrt.putwch( u"\b" )
                msvcrt.putwch( u"\b" )
                msvcrt.putwch( u" "  )
                msvcrt.putwch( u"\b" )
            elif state==2:
                # ���� 1 
                # ���ʱ�ȭ
                state=1
                jung=None;
                ime_wprint(asm(cho,jung,jong),2)
            elif state==3:
                # ����2 
                state=2
                jung=jung1
                jung1=None;jung2=None
                ime_wprint(asm(cho,jung,jong),2)
            elif state==4:
                # ����2
                # ���ʱ�ȭ
                state=2
                jong=None
                ime_wprint(asm(cho,jung,jong),2)
            elif state==5:
                # ��1��2 �ʱ�ȭ
                # ����4
                # ����2 
                state=4
                jong=jong1
                jung1=None;jung2=None
                ime_wprint(asm(cho,jung,jong),2)
            continue 
                
        if not jm : 
            # �ڸ��̿ܿ� �ش��ϴ� ���ڰ� �Է� �Ǿ���
            # ������ �����ϴ� ���ڸ� �ϼ�
            # Ư��������� 
            # ���ο� �������� �Ѿ 
            if state != 0 :
                input_list.append( asm(cho,jung,jong) )
            if isprint(c):
                new_u = unicode( c, ENCODING )
                ime_wprint( new_u )
                input_list.append( new_u )
            state=0
            cho=None; jung=None; jong=None 
            continue 
        if state == 0 : #--------------- ���ۻ���
            if is_jaum(jm) :
                cho = jm         
                state = 1
                ime_wprint(asm(cho,jung,jong))
            else :
                cho = None
                jung = jm
                state = 2
                ime_wprint(asm(cho,jung,jong))
        elif state == 1 :#--------------- �ʼ��� �ϼ��� ����
            if is_jaum(jm): #������ �Է�        
                # ���ڰ� �ϼ��Ǿ��� 
                #ȭ�鿡 �ϼ��� ���ڸ� ����ϰ� 
                #���� ���ڷ� �Ѿ�鼭 
                #���� �Էµ� ���ڴ� ������ �Ǿ�� �Ѵ�.            
                state = 1
                input_list.append( cho )
                cho=jm; jung=None; jong=None
                ime_wprint( asm(cho,jung,jong) )
            else:
                #������ �Էµ� 
                jung = jm
                state = 2
                uc = asm(cho,jung,jong) 
                ime_wprint(uc,2)
        elif state == 2 : #--------------- �߼����� �Էµ� ����
            if is_jaum(jm):
                if cho:
                    # ������ ���� 
                    # ȭ�鿡 �ϼ��� ���ڸ� ����ϰ�
                    # ���� ����� ���ڴ� �����̹Ƿ� 
                    # ���´� 4
                    # ������ ���ε��� �����Ҵ�
                    state=4
                    jong=jm
                    ime_wprint(asm(cho,jung,jong),2)
                else:
                    input_list.append( jung )
                    state=1                    
                    cho=jm;jung=None;jong=None
                    ime_wprint(asm(cho,jung,jong),2)                
            else :      
                #������ ���� 
                new_jm = asm_jm(jung,jm)
                if new_jm :  #���߸��� �Ǻ�
                    state = 3 
                    jung1=jung;
                    jung2=jm
                    jung = new_jm
                    ime_wprint(asm(cho,jung,jong),2)
                else : #���߸��� x
                    # ���ο� ���ڰ� �ϼ��Ǿ��� 
                    # ȭ�鿡 �ϼ��� ���ڸ� ����ϰ�
                    # ���� ����� ���ڴ� �����̹Ƿ� 
                    # ���´� 2
                    # �ʼ��� ����
                    # �߼��� ������ڸ� �Ҵ� 
                    input_list.append( asm(cho,jung,jong) )
                    state = 2
                    cho = None; jung=jm; jong=None   
                    ime_wprint(asm(cho,jung,jong))
        elif state == 3: #--------------- �߼����� ���߸����� �Էµ� ����
            if is_jaum(jm) :
                if cho and asm(cho,jung,jm): #��+��+������ �ѱۿϼ����� �Ǻ� 
                    state = 4 
                    jong = jm
                    ime_wprint(asm(cho,jung,jong),2)
                else:
                    # ���ο� ���ڰ� �ϼ��Ǿ���
                    # ȭ�鿡�ϼ��� ���ڸ� ����ϰ�
                    # ���ε��� ���ڴ� �����̹Ƿ�
                    # �ʼ��� �Ҵ�
                    # ���´� 1
                    input_list.append( jung )
                    state = 1 
                    cho=jm; jung=None; jong=None
                    ime_wprint(asm(cho,jung,jong))                
            else:
                # ���ο� ���ڰ� �ϼ��Ǿ���
                # ȭ�鿡 �ϼ��� ���ڸ� ����ϰ� 
                # ���� ���� ���ڴ� �����̱� ������  
                # ���´� 2
                # �ʼ��� ����
                # �߼��� ������ڸ� �Ҵ� 
                input_list.append( asm(cho,jung,jong) )
                state = 2 
                cho=None; jung=jm; jong=None
                ime_wprint(asm(cho,jung,jong))
        elif state == 4: #--------------- �������� �Էµ� ����
            if is_jaum(jm):
                new_jm = asm_jm(jong,jm) #������ �������� ���ɼ� �Ǻ�
                if new_jm and asm(cho,jung,jong): 
                    # ȭ�鿡 �ϼ��� ���ڸ� ����ϰ�
                    # ���´� 5
                    jong1=jong; jong2=jm
                    jong=new_jm
                    ime_wprint(asm(cho,jung,jong),2)
                    state = 5
                else:
                    # ���ο� ���ڰ� �ϼ��Ǿ���
                    # ȭ�鿡 �ϼ��� ���ڸ� ����ϰ�
                    # �������� ���� 
                    # ���´� 1
                    ime_wprint(asm(cho,jung,jong),2)
                    input_list.append( asm(cho,jung,jong) )
                    state=1 
                    cho=jm; jung=None; jong=None
                    ime_wprint(asm(cho,jung,jong))                
            else:    
                # �� ���¿��� ������ �Էµ�
                # �ʼ� �߼����� ���ڸ� �ϼ� �ϰ�
                # ���� , ���� -> �ʼ� �߼����� ����
                # ���´� 2�� ������ �� 
                ime_wprint(asm(cho,jung,None),2)  
                input_list.append( asm(cho,jung,None) )
                state=2 
                cho=jong; jung=jm; jong=None
                ime_wprint( asm(cho,jung,jong))            
        elif state == 5: #--------------- ���� ������������ �Էµ� ���� 
            if is_jaum(jm):
                # ������ �ԷµǾ���
                # �������ڴ� �״�� �ΰ�
                # �����Էµ� �������� �������
                # ���´� 1
                input_list.append( asm(cho,jung,jong) )
                cho = jm;jung = None ;jong=None
                ime_wprint(asm(cho,jung,jong))
                state=1            
            else:
                # ������ �ԷµǾ���
                # ��,��,ù��°�������� ���ο� ���ڿϼ� �Ͽ� ȭ�鿡 ���
                # ���������������� �����Էµ� �������� �ʼ��߼��� �ϼ�
                # ���´� 2
                ime_wprint(asm(cho,jung,jong1),2)  
                input_list.append( asm(cho,jung,jong1) )
                cho = jong2;jung = jm ;jong=None
                ime_wprint(asm(cho,jung,jong))
                state = 2     