grammar Calculator;

options {
    language = Java;
}

@members {
    public static final String NUM        = "00000000";
    public static final String MUVELET     = "00000001";
    public static final String VALTOZO    = "00000010";
    public static final String ERTEKADAS   = "00000011";

    public static final String ADD         = "00000000";
    public static final String SUB         = "00000001";
    public static final String MUL         = "00000010";
    public static final String DIV         = "00000011";

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
    : REGISTER '=' expr 
    | expr 
    ;



expr 
    : lhs=addop (OPADD lhs=addop { System.out.print(MUVELET+($OPADD.text.equals("+")?ADD:SUB)); } )?
    ;

addop 
    : lhs=mulop  (OPMUL lhs=mulop { System.out.print(MUVELET+($OPMUL.text.equals("*")?MUL:DIV)); })?
    ;

mulop 
    : fct  (OPMUL fct { System.out.print(MUVELET+($OPMUL.text.equals("*")?MUL:DIV)); })?
    ;

fct  
    : SZAM { System.out.print(NUM + toByteString($SZAM.int)); }
    | '(' expr ')' 
    | REGISTER { System.out.print(Integer.parseInt($REGISTER.text.substring(2,3))); }
    ;

LF       : '\n' ;
WS       : [ \t\r]+ ->skip ;
SZAM     : [0-9]+('.' [0-9]+)? ;
OPADD    : '+' | '-' ;
OPMUL    : '*' | '/' ;
REGISTER   : 'm['([0-9]|[1-9][0-9])']';
