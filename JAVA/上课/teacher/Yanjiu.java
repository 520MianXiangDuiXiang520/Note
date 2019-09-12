package teacher;
import teacher.Student;

public class Yanjiu extends Student {
	String article;
	public Yanjiu(teacher tea, String no, String name, String art){
		super(tea, no, name);
		this.article = art;
	}
    public void printArticle(){
    	this.printInfo();
    	System.out.println("бшнд: " + this.article);
    }
}
