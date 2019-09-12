package teacher;

public class teacher {
	String ID;
	String name;
	public teacher(String no,String name){
		this.ID = no;
		this.name = name;
	}
	public void printInfo(){
		System.out.println("teacher name: " + this.name + "  ID: " + this.ID);
	}
    
}
