//
//  LoginViewController.m
//  CylinderParking
//
//  Created by Adrian Duran on 24/11/14.
//  Copyright (c) 2014 AD. All rights reserved.
//

#import "LoginViewController.h"

#import "MBProgressHUD.h"

@interface LoginViewController ()

@end

@implementation LoginViewController

- (void) viewWillAppear:(BOOL) animated
{
    [super viewWillAppear:animated];
    [self.errorLabel setHidden:YES];
}

- (IBAction)onDismissKeyboardButton:(id)sender {
    [self.usernameTextField resignFirstResponder];
    [self.passwordTextField resignFirstResponder];
}

- (IBAction)onLoginButtonTUI:(id)sender {
    
    [self.usernameTextField resignFirstResponder];
    [self.passwordTextField resignFirstResponder];
    
    [self.errorLabel setHidden:YES];
    
    [MBProgressHUD showHUDAddedTo:self.view animated:YES];
    
    if ([self.usernameTextField.text isEqualToString:@"admin"] && [self.passwordTextField.text isEqualToString:@"admin1234"]) {
        // Make request to get cylinder info
        [self performSegueWithIdentifier:@"showCylinderSegue" sender:nil];
    }
    else {
        [self.errorLabel setText:@"Error: Wrong username and password combination"];
        [self.errorLabel setHidden:NO];
        
        [MBProgressHUD hideHUDForView:self.view animated:YES];
    }
    
}

@end
