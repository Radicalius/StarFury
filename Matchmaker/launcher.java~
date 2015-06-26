import java.io.*;
import java.awt.*;
import java.awt.geom.*;
import java.awt.event.*;
import javax.swing.*;
import java.net.*;

class launcher{

	static JFrame f;

	static class LobbyScreen extends JPanel{
		JTextArea jt;
		JScrollPane sp;
	public LobbyScreen(){
		//setLayout(null);
		jt = new JTextArea();
		sp = new JScrollPane(jt);
		//sp.setBounds(0,480,860,200);
		this.add(sp);
	}
	}

	static class LoginScreen extends JPanel implements ActionListener{
		int mode = 0;
		JLabel title;
		JTextField user;
		JPasswordField pass;
		JButton submit;
		BufferedReader bf;
		PrintStream ps;
		JFrame master;
		JLabel u;
		JLabel p;
		Socket s;
	public LoginScreen(JFrame master1){
		this.setLayout(null);
		title = new JLabel("Launcher");
		title.setFont(new Font("Exo",0,50));
		this.add(title);
		title.setBounds(320+25,240-100,300,50);
		user = new JTextField();
		this.add(user);
		user.setBounds(320,240+50,300,20);
		user.setFont(new Font("Exo",0,18));
		pass = new JPasswordField();
		this.add(pass);
		pass.setBounds(320,240+75,300,20);
		pass.setFont(new Font("Exo",0,18));
		u = new JLabel("Username");
		u.setFont(new Font("Exo",0,18));
		u.setBounds(320-12*8,240+50,300,20);
		add(u);
		p = new JLabel("Password");
		p.setFont(new Font("Exo",0,18));
		p.setBounds(320-12*8,240+75,300,20);
		add(p);
		submit = new JButton("Log In");
		submit.setFont(new Font("Exo",0,15));
		submit.setActionCommand("Submit");
		submit.setBounds(320+75,240+155,100,20);
		submit.addActionListener(this);
		add(submit);
		master = master1;
	}
	public void actionPerformed(ActionEvent e){
		String cmd = e.getActionCommand();
		if (mode == 0 && cmd.equals("Submit")){
			//try{
				//s = new Socket(InetAddress.getByName("localhost"),8001);
				//ps = new PrintStream(s.getOutputStream());
				//bf = new BufferedReader(new InputStreamReader(s.getInputStream()));
				//String asd = user.getText()+":"+pass.getText();
				//ps.print(asd.length());
			//	ps.print(asd);
				//while (!bf.ready()){ System.out.println("in");}
				//int code = Integer.parseInt(bf.readLine());
				//if (code == 1){
				if (true){
					mode = 1;
					f.remove(this);
					//f.setLayout(null);
					JTextArea a = new JTextArea();
					JScrollPane p = new JScrollPane(a);
					//p.setBounds(0,0,540,400);
					f.add(p);
					f.repaint();
					
				}
			//}catch (IOException j){ System.out.println(j); }
		}
	}
	}

	public static void main(String[] args){
		f = new JFrame("Launcher");
		f.setSize(860,680);

		LoginScreen s = new LoginScreen(f);
		f.add(s);

		f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		f.setVisible(true);
	}
}
