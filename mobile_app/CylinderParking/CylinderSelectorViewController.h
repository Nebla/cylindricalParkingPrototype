//
//  CylinderSelectorViewController.h
//  CylinderParking
//
//  Created by Adrian Duran on 24/11/14.
//  Copyright (c) 2014 AD. All rights reserved.
//

#import <UIKit/UIKit.h>

#import "ViewController.h"

@interface CylinderSelectorViewController : UIViewController <UITableViewDataSource, UITableViewDelegate>

@property(nonatomic) ViewController* cylinder;

@end
