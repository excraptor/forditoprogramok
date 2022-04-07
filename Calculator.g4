grammar Calculator;

options {
    language = Java;
}

@members {
    public static final String NUM         = "00000000";
    public static final String MUVELET     = "00000001";
    public static final String VALTOZO     = "00000010";
    public static final String ERTEKADAS   = "00000011";
    public static final String READ        = "00000100";

    // public static final String NUM         = "SZAM";
    // public static final String MUVELET     = "MUVELET";
    // public static final String VALTOZO     = "VALTOZO";
    // public static final String ERTEKADAS   = "ERTEKADAS";

    public static final String ADD         = "00000000";
    public static final String SUB         = "00000001";
    public static final String MUL         = "00000010";
    public static final String DIV         = "00000011";

    // public static final String ADD         = "ADD";
    // public static final String SUB         = "SUB";
    // public static final String MUL         = "MUL";
    // public static final String DIV         = "DIV";

    public String toByteString(int n) {
        String res = "";
        while(n != 0) {
            res += n%2;
            n = n/2;
        }
        if(res.length() < 8) {
            int remaining = 8-res.length();
            for(int i = 0; i < remaining; i++) {
                res += "0";
            }
        }

        return new StringBuilder(res).reverse().toString();
    }

    public int extractNumbers(String str, boolean isRegister) { 
        char beginParentheses = isRegister? '[' : '(';
        char endParentheses = isRegister? ']' : ')';
        String number = str.substring(str.indexOf(beginParentheses)+1, str.indexOf(endParentheses));
        //System.out.println("valtozo szam: " + number);
        return Integer.parseInt(number);
    }


    public static void main(String[] args) throws Exception {
        CalculatorLexer lex = new CalculatorLexer(new ANTLRFileStream(args[0]));
        CommonTokenStream tokens = new CommonTokenStream (lex);
        CalculatorParser parser = new CalculatorParser(tokens);
        parser.start();
    }
}

start
    : (line? LF)* EOF
    ;

line
    : REGISTER 
    { System.out.print(VALTOZO + toByteString(extractNumbers($REGISTER.text, true))+ERTEKADAS); }
    '=' expr {System.out.print("\n");}
    | expr {System.out.print("\n");}
    ;



expr 
    : addop (OPADD addop { System.out.print(MUVELET+($OPADD.text.equals("+")?ADD:SUB)); })*
    ;

addop 
    : fct  (OPMUL addop { System.out.print(MUVELET+($OPMUL.text.equals("*")?MUL:DIV)); })*
    ;


fct  
    : SZAM { System.out.print(NUM + toByteString($SZAM.int)); }
    | '(' expr ')' 
    | REGISTER { System.out.print(VALTOZO + toByteString(extractNumbers($REGISTER.text, true))); }
    | READOP { System.out.print(READ + toByteString(extractNumbers($READOP.text, false))); }
    ;

LF       : '\n' ;
WS       : [ \t\r]+ ->skip ;
SZAM     : [0-9]+('.' [0-9]+)? ;
OPADD    : '+' | '-' ;
OPMUL    : '*' | '/' ;
REGISTER : 'm[' ([0-9]|[1-9][0-9]) ']';
READOP    : 'read(' ([0-9]|[1-9][0-9]) ')';
