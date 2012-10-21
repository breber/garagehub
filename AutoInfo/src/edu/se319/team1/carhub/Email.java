package edu.se319.team1.carhub;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.google.appengine.api.mail.MailService;
import com.google.appengine.api.mail.MailService.Message;
import com.google.appengine.api.mail.MailServiceFactory;

/**
 * Class containing static methods for sending emails
 */
public class Email {
	private static final Logger log = Logger.getLogger(Email.class.getName());

	/**
	 * Sends an email to the given email addresses with the given message and subject
	 * 
	 * @param subject the subject of the email
	 * @param message the body of the email
	 * @param replyToAddress the address to set as the reply to
	 * @param replyToName the name to use as a reply to
	 * @param addresses the addresses to send the message to
	 */
	public static void sendEmail(String subject, String message, String replyToAddress, String replyToName, String ... addresses) {
		MailService service = MailServiceFactory.getMailService();

		Message msg = new Message();
		msg.setSender("reber.brian@gmail.com");

		if (replyToAddress != null && replyToName != null) {
			msg.setReplyTo(replyToAddress);
		}

		msg.setSubject(subject);
		msg.setHtmlBody((message == null) ? "" : message.toString());

		List<String> to = new ArrayList<String>();
		for (String current : addresses) {
			if (current.contains("@")) {
				to.add(current);
			}
		}
		msg.setTo(to);

		try {
			service.send(msg);
		} catch (IOException e) {
			log.log(Level.WARNING, "Error emailing - sendEmail");
			e.printStackTrace();
		}
	}

	/**
	 * Sends an email to Brian
	 * 
	 * @param subject the subject of the message
	 * @param message the content of the message
	 */
	public static void sendEmailToBrian(String subject, String message) {
		MailService service = MailServiceFactory.getMailService();

		Message msg = new Message();
		msg.setSender("reber.brian@gmail.com");

		msg.setSubject(subject);
		msg.setHtmlBody((message == null) ? "" : message.toString());
		msg.setTo("reber.brian@gmail.com");

		try {
			service.send(msg);
		} catch (IOException e) {
			log.log(Level.WARNING, "Error emailing - sendEmail");
			e.printStackTrace();
		}
	}
}
