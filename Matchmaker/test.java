import javax.swing.*;
import java.awt.event.*;
import java.awt.*;
import java.io.*;
import java.net.*;
import java.lang.*;
import java.util.*;

public class test{

	static JTextArea a;
	static JTextField k;
	static BufferedReader bf;
	static PrintStream ps;
	static JScrollPane fsp;
	static JScrollPane csp;
	static JTextArea friends;
	static JPanel comps;
	static int port = 8006;	
	static HashMap<String,String> fri;

	static class CompIcon extends JPanel implements MouseMotionListener,MouseListener{
		String name;
		ArrayList<String> bufs;
		ImageIcon img;
		boolean selected;
		int mx;
		int my;
		int y;
	public CompIcon(File f,int y){
		this.y = y;
		selected = false;
		try{
			bufs = new ArrayList<String>();
			BufferedReader in = new BufferedReader(new InputStreamReader(new FileInputStream(f)));
			while (in.ready()){
				String inp = in.readLine();
				inp = inp.replace("\n","");
				String[] g = inp.split(" ");
				String[] i = inp.split("=");
				System.out.println(i.length);
				if (i.length>1){
					System.out.println(i[0]);
					if (i[0].equals("Name")){
						name = i[1];
					}if (i[0].equals("Image")){
						img = new ImageIcon("../Images/"+i[1]);
						System.out.println("../Images/"+i[1]);
					}
				}if (g.length>1){
					bufs.add(g[0]+" "+g[1]);
				}
			}
			
		}catch (IOException e){ System.out.println(e);}
	}
	public void paintComponent(Graphics g){
		Graphics2D screen = (Graphics2D)g;
		screen.setColor(new Color(255,255,255));
		if (!selected){
			screen.fillRect(0,0,150,75);
		}else{
			screen.setColor(new Color(0,255,0));
			screen.fillRect(0,0,150,75);
			screen.setColor(new Color(255,255,255));
			screen.fillRect(5,5,140,65);
		}
		img.paintIcon(this,g,0,0);
		screen.setColor(Color.black);	
		screen.drawString(name,63,20);	
		int x = 35;
		for (String b:bufs){
			screen.drawString(b,63,x);
			x+=15;	
		}
	}
	public void mouseMoved(MouseEvent e){
		mx = e.getX();
		my = e.getY();
	}
	public void mouseDragged(MouseEvent e){}
	public void mouseExited(MouseEvent e){}
	public void mouseEntered(MouseEvent e){}
	public void mousePressed(MouseEvent e){}
	public void mouseReleased(MouseEvent e){}
	public void mouseClicked(MouseEvent e){
		if (my>y && my<y+80){
			selected = !selected;
		}else{
			selected = false;
		}
		System.out.println("in");
		repaint();
	}
	}

	static class recvthread implements Runnable{
		Thread t;
	public recvthread(){
		t = new Thread(this);
		t.start();
	}
	public void run(){
		while (true){
			try{
				if (bf.ready()){
					String inp = bf.readLine();
					if (inp.toCharArray()[0] == '/'){
						String[] g = inp.split(" ");
						if (g[0].equals("/user")){
							fri.put(g[1],g[2]);
							String text = "";
							for (String i:fri.keySet()){
								text+=i+" "+fri.get(i)+"\n";
							}
							friends.setText(text);
						}if (g[0].equals("/friend")){
							int response = JOptionPane.showConfirmDialog(null,g[1]+" has invited you to see his/her presence online.","Friend Invite",JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE);
							if (response == JOptionPane.YES_OPTION){
								ps.print("02/y");
							}else{
								ps.print("02/n");
							}
						}
					}else{
						a.setText(a.getText()+inp+"\n");
						System.out.println(inp);
					}
				}
			}catch(IOException e){ System.out.println(e);}
		}
	}
	}

	static class listener implements ActionListener{
	public void actionPerformed(ActionEvent e){
		String text = k.getText();
		k.setText("");
		if (text.length()<10){
			ps.print("0"+Integer.toString(text.length())+text);
		}else{
			ps.print(Integer.toString(text.length())+text);
		}
	}
	}

	public static void main(String[] args){
		JFrame f = new JFrame();
		f.setResizable(false);
		f.setSize(880,680);
		f.setLayout(null);
		a = new JTextArea();
		a.setText("/register [username] [password]\n/login [username] [password]\n");
		k = new JTextField();
		k.setBounds(150,480+145,860-300,20);
		a.setEditable(false);
		JScrollPane p = new JScrollPane(a);
		p.setBounds(150,480,860-300,145);
		friends = new JTextArea();
		friends.setEditable(false);
		fsp = new JScrollPane(friends);
		fsp.setBounds(0,0,150,680);
		comps = new JPanel();
		//comps.setLayout(null);
		csp = new JScrollPane(comps);
		csp.setBounds(860-150,0,170,680);
		f.add(csp);
		f.add(p);
		f.add(k);
		f.add(fsp);
		listener l = new listener();
		k.addActionListener(l);
		f.setVisible(true);
		int y = 0;
		for (File i:new File("../Components").listFiles()){
			CompIcon t = new CompIcon(i,y*80);
			t.setBounds(0,y*80,150,80);
			comps.add(t);
			comps.addMouseMotionListener(t);
			comps.addMouseListener(t);
			y++;
		}
		try{
			Socket s = new Socket(InetAddress.getByName("localhost"),port);
			bf = new BufferedReader(new InputStreamReader(s.getInputStream()));
			ps = new PrintStream(s.getOutputStream());
		}catch (IOException e){ System.out.println(e);}
		recvthread rt = new recvthread();
		fri = new HashMap<String,String>();
		f.addWindowListener(new java.awt.event.WindowAdapter() {
			@Override
    			public void windowClosing(java.awt.event.WindowEvent windowEvent) {
				ps.print("07/logout");
			}
		});
	}
}
