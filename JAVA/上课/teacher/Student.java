package teacher;
import teacher.teacher;

public class Student {
	public teacher tutor;
	public String ID;
	public String name;
	
	public Student(teacher tea, String no, String name){
		this.tutor = tea;
		this.ID = no;
		this.name = name;
	}
	public void printInfo(){
		System.out.print("student name: " + this.name + "  ID: " + this.ID);
		this.tutor.printInfo();
	}
    static public void main(String []args){
    	
    }
}
