//
//  ViewController.h
//  CylinderParking
//
//  Created by Adrian Duran on 24/11/14.
//  Copyright (c) 2014 AD. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface ViewController : UIViewController <UICollectionViewDataSource, UICollectionViewDelegate> {
    
    __weak IBOutlet UIButton *cylinderButton;
    __weak IBOutlet UICollectionView *cylinderView;
}

- (void) selectedNewCylinder:(NSInteger)cylinder;

@end

