package teacher;
import teacher.Student;
import teacher.teacher;
import teacher.Yanjiu;

public class main {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		teacher t1 = new teacher( "200310", "lisi");
		Student s1 = new Student(t1, "1707005644", "zhangsan");
		Student s2 = new Student(t1, "1707005645", "wangwu");
		Student s3 = new Student(t1, "1707005646", "zhaoliu");
		Yanjiu y1 = new Yanjiu(t1,"160000", "xiaowang", "JAVA");
		
		s1.printInfo();
		s2.printInfo();
		s3.printInfo();
		y1.printArticle();
	}

}
