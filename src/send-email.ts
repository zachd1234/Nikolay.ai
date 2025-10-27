#!/usr/bin/env node

import { Command } from 'commander';
import nodemailer from 'nodemailer';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

const program = new Command();

program
  .name('send-email')
  .description('CLI tool to send emails via Gmail')
  .requiredOption('--to <email>', 'Recipient email address')
  .requiredOption('--subject <subject>', 'Email subject line')
  .requiredOption('--body <html>', 'Email body (supports HTML/rich text)')
  .option('--cc <email>', 'CC email address (optional)')
  .parse(process.argv);

const options = program.opts();

async function sendEmail() {
  try {
    // Validate environment variables
    if (!process.env.GMAIL_USER || !process.env.GMAIL_APP_PASSWORD) {
      throw new Error('Missing Gmail credentials in .env file. Please set GMAIL_USER and GMAIL_APP_PASSWORD.');
    }

    // Create transporter
    const transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: process.env.GMAIL_USER,
        pass: process.env.GMAIL_APP_PASSWORD.replace(/\s/g, ''), // Remove spaces from app password
      },
    });

    // Verify connection
    console.log('Verifying Gmail connection...');
    await transporter.verify();
    console.log('✓ Connected to Gmail successfully\n');

    // Convert line breaks to HTML
    const htmlBody = options.body.replace(/\n/g, '<br>');

    // Prepare email options
    const mailOptions: nodemailer.SendMailOptions = {
      from: `Sundai Hacks <${process.env.GMAIL_USER}>`,
      to: options.to,
      subject: options.subject,
      html: htmlBody,
    };

    // Add CC if provided
    if (options.cc) {
      mailOptions.cc = options.cc;
    }

    // Send email
    console.log('Sending email...');
    console.log(`  To: ${options.to}`);
    if (options.cc) {
      console.log(`  CC: ${options.cc}`);
    }
    console.log(`  Subject: ${options.subject}\n`);

    const info = await transporter.sendMail(mailOptions);

    console.log('✓ Email sent successfully!');
    console.log(`  Message ID: ${info.messageId}`);
    console.log(`  Response: ${info.response}`);

  } catch (error) {
    console.error('✗ Error sending email:');
    if (error instanceof Error) {
      console.error(`  ${error.message}`);
    } else {
      console.error(error);
    }
    process.exit(1);
  }
}

sendEmail();
