class MyStudent{
	static int auth_id = 1;
	int id;
	String name;
	public Student(String name){
		this.name = name;
		this.id = auth_id;
		auth_id ++;
	}
	public void println(){
		System.out.println(this.id + ": " + this.name);
	}
}
public class Student {
	static public void main(String [] args){
       MyStudent s1 = new MyStudent("zhangsan");
       s1.println();
       MyStudent s2 = new MyStudent("lisi");
       s2.println();
	}
}
