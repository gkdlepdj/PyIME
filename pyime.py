#-*- coding: cp949 -*-   
import msvcrt
# ����� �α׿�
import logging
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
    logging.debug("asm(), %s,%s,%s",dcho,djung,djong)
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
        ����Ű �Է½� ���� ���������� �Ѵ�  
        
    @�Ķ����: u_code: Ÿ���� �����ڵ�,����ϰ��� �ϴ� ����(1��)
    @�Ķ����: bs: Ÿ���� ����,�齺���̽� Ƚ�� 
               �� ���ڸ� ����� ���ؼ� 2ȸ�� �齺���̽��� �����ؾ� �Ѵ�. 
    """
    logging.debug("ime_wprint,u_code:%s",u_code.encode(ENCODING))
    for i in range(bs):
        msvcrt.putwch( u"\b" )
    # ����Ű �Է½� ���� �������� 
    if ord(u_code) == 13:
        msvcrt.putch('\r')
        msvcrt.putch('\n')
        return 
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
jong1 = None  #���߸��� ù��° ����
jong2 = None  #���߸��� �ι�° ����


while True :
    c = msvcrt.getch()
    jm = engkey2kor(c)
    if jm :
        logging.debug("engkey2kor(),%s", jm.encode(ENCODING) )
    else :
        logging.debug("engkey2kor()- not eng ==> %s(%d)", c,ord(c) ) 
    if not jm : 
        #�ڸ��̿ܿ� �ش��ϴ� ���ڰ� �Է� �Ǿ���
        #������ �����ϴ� ���ڸ� �ϼ�
        #Ư��������� 
        #���ο� �������� �Ѿ 
        ime_wprint( unicode( c, ENCODING ) )
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
            cho=jm; jung=None; jong=None
            ime_wprint(asm(cho,jung,jong))
        else:#������ �Էµ� 
            jung = jm
            state = 2
            uc = asm(cho,jung,jong) 
            # logging.debug("text:%s uc:%s","������ �Է�",uc)
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
                state=1
                cho=jm;jung=None;jong=None
                ime_wprint(asm(cho,jung,jong),2)                
        else :      
            #������ ���� 
            new_jm = asm_jm(jung,jm)
            if new_jm :  #���߸��� �Ǻ�
                state = 3 
                jung = new_jm
                ime_wprint(asm(cho,jung,jong),2)
            else : #���߸��� x
                # ���ο� ���ڰ� �ϼ��Ǿ��� 
                # ȭ�鿡 �ϼ��� ���ڸ� ����ϰ�
                # ���� ����� ���ڴ� �����̹Ƿ� 
                # ���´� 2
                # �ʼ��� ����
                # �߼��� ������ڸ� �Ҵ� 
                ime_wprint(asm(cho,jung,jong),2)
                state = 2
                cho=None; jung=jm; jong=None   
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
                ime_wprint(asm(cho,jung,jong),2)
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
            ime_wprint(asm(cho,jung,jong),2)
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
                state=1 
                cho=jm; jung=None; jong=None
                ime_wprint(asm(cho,jung,jong))                
        else:    
            # �� ���¿��� ������ �Էµ�
            # �ʼ� �߼����� ���ڸ� �ϼ� �ϰ�
            # ���� , ���� -> �ʼ� �߼����� ����
            # ���´� 2�� ������ �� 
            ime_wprint(asm(cho,jung,None),2)
            state=2 
            cho=jong; jung=jm; jong=None
            ime_wprint( asm(cho,jung,jong))            
    elif state == 5: #--------------- ���� ������������ �Էµ� ���� 
        if is_jaum(jm):
            # ������ �ԷµǾ���
            # �������ڴ� �״�� �ΰ�
            # �����Էµ� �������� �������
            # ���´� 1
            cho = jm;jung = None ;jong=None
            ime_wprint(asm(cho,jung,jong))
            state=1            
        else:
            # ������ �ԷµǾ���
            # ��,��,ù��°�������� ���ο� ���ڿϼ� �Ͽ� ȭ�鿡 ���
            # ���������������� �����Էµ� �������� �ʼ��߼��� �ϼ�
            # ���´� 2
            ime_wprint(asm(cho,jung,jong1),2)
            cho = jong2;jung = jm ;jong=None
            ime_wprint(asm(cho,jung,jong))
            state = 2     