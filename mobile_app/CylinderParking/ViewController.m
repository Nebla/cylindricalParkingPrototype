//
//  ViewController.m
//  CylinderParking
//
//  Created by Adrian Duran on 24/11/14.
//  Copyright (c) 2014 AD. All rights reserved.
//

#import "ViewController.h"

#import "FPPopoverController.h"
#import "PlatformCollectionViewCell.h"
#import "CylinderSelectorViewController.h"
#import "SlotTableViewCell.h"
#import "MBProgressHUD.h"

#define COLUMNS 3
#define LEVELS 5

@interface ViewController ()

@end

@implementation ViewController

- (void) viewWillAppear:(BOOL) animated
{
    [super viewWillAppear:animated];
    currentCylinder = 0;
    [cylinderButton setTitle:@"Cylinder 0" forState:UIControlStateNormal];
    
    vehicles = [[NSMutableArray alloc] init];
    parkingSlot = [[NSMutableArray alloc] init];
    
    [vehicles addObject:[self getOneCylinder]];
    [vehicles addObject:[self getOneCylinder]];
    [vehicles addObject:[self getOneCylinder]];
    
    [parkingSlotView setHidden:YES];
    
    //the view controller you want to present as popover
    UIStoryboard *sb = [UIStoryboard storyboardWithName:@"Main" bundle:nil];
    CylinderSelectorViewController *controller = (CylinderSelectorViewController *)[sb instantiateViewControllerWithIdentifier:@"CylinderSelectorViewController"];
    controller.cylinder = self;
    //our popover
    popover = [[FPPopoverController alloc] initWithViewController:controller];
}

- (NSMutableArray *)getOneCylinder {
    NSMutableArray *cilinder = [[NSMutableArray alloc] init];
    for (int i = 0; i < COLUMNS * LEVELS; ++i) {
        NSString *patente = @"";
        UIColor *color = [UIColor colorWithRed:150/255.0 green:150/255.0 blue:170/255.0 alpha:1];
        
        NSString *imageName = [self getRandomImage];
        
        if (imageName != nil) {
            int randNum = rand() % (999 - 100) + 100; //create the random number.
            NSString *randString = [self randomStringWithLength:3];
            int randColor = rand() % (5 - 1) + 1;
            
            patente = [NSString stringWithFormat:@"%@-%d",randString,randNum];
            color = [self getColor:randColor];
        }
        else {
            imageName = @"";
        }
        NSDictionary *dic = [[NSDictionary alloc] initWithObjectsAndKeys:patente,@"patente",imageName,@"imagen",color,@"color", nil];
        [cilinder addObject:dic];
    }
    return cilinder;
}

- (NSString *) getRandomImage {
    int randImage = rand() % (8); //create the random number.
    
    switch (randImage) {
        case 0:
            return @"MotoSide.png";
            break;
        case 1:
            return @"CarSide.png";
            break;
        case 2:
            return @"AutoTruckSide.png";
            break;
        case 3:
            return @"TrukSide.png";
            break;
        default:
            return nil;
            break;
    }
    return nil;
}


-(NSString *) randomStringWithLength: (int) len {
    NSString *letters = @"ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    NSMutableString *randomString = [NSMutableString stringWithCapacity: len];
    
    for (int i=0; i<len; i++) {
        [randomString appendFormat: @"%C", [letters characterAtIndex: arc4random_uniform([letters length])]];
    }
    
    return randomString;
}

- (void) selectedNewCylinder:(NSInteger)cylinder {
    
    currentCylinder = cylinder;

    [MBProgressHUD showHUDAddedTo:self.view animated:YES];
    [self performSelector:@selector(changeCylinder) withObject:nil afterDelay:1];
    
    [popover dismissPopoverAnimated:YES];
}

- (void) changeCylinder {
    // Get new cylinder info
    if (currentCylinder < 3) {
        [cylinderButton setTitle:[NSString stringWithFormat:@"Cylinder %ld",(long)currentCylinder] forState:UIControlStateNormal];
        [cylinderView reloadData];
        [cylinderView setHidden:NO];
        [parkingSlotView setHidden:YES];
    }
    else {
        [cylinderButton setTitle:@"Parking Slot" forState:UIControlStateNormal];
        [parkingSlotView reloadData];
        [cylinderView setHidden:YES];
        [parkingSlotView setHidden:NO];
    }
    [MBProgressHUD hideHUDForView:self.view animated:YES];
    
}

- (IBAction)onSelectCylinderTUI:(id)sender {
    //the popover will be presented from the okButton view
    [popover presentPopoverFromView:sender];
}

- (UIColor *)getColor:(NSInteger)index {
    UIColor *backgroundColor = [UIColor colorWithRed:150/255.0 green:150/255.0 blue:150/255.0 alpha:1];
    switch (index) {
        case 1:
            backgroundColor = [UIColor colorWithRed:100/255.0 green:100/255.0 blue:255/255.0 alpha:1];
            break;
        case 2:
            backgroundColor = [UIColor colorWithRed:255/255.0 green:100/255.0 blue:100/255.0 alpha:1];
            break;
        case 3:
            backgroundColor = [UIColor colorWithRed:150/255.0 green:100/255.0 blue:255/255.0 alpha:1];
            break;
        case 4:
            backgroundColor = [UIColor colorWithRed:200/255.0 green:100/255.0 blue:255/255.0 alpha:1];
            break;
        case 5:
            backgroundColor = [UIColor colorWithRed:255/255.0 green:100/255.0 blue:255/255.0 alpha:1];
            break;
        default:
            break;
    }
    return backgroundColor;
}

- (void)collectionView:(UICollectionView *)collectionView didSelectItemAtIndexPath:(NSIndexPath *)indexPath {
    if (currentCylinder < 3) {
        selectedIndex = indexPath.row;
        NSString *patente = [[[vehicles objectAtIndex:currentCylinder] objectAtIndex:indexPath.row] objectForKey:@"patente"];
        
        if ([patente length] > 0) {
            NSString *msg = [NSString stringWithFormat:@"Do you want to withdraw vehicle %@",patente];
            
            UIAlertView *alert = [[UIAlertView alloc] initWithTitle:@"Confirmation" message:msg delegate:self cancelButtonTitle:@"Acept" otherButtonTitles:@"Cancel", nil];
            [alert show];
        }
    }
}

- (void)alertView:(UIAlertView *)alertView clickedButtonAtIndex:(NSInteger)buttonIndex {
    if (buttonIndex == 0) {

        NSMutableDictionary *withdrawCar = [[vehicles objectAtIndex:currentCylinder] objectAtIndex:selectedIndex];
        [parkingSlot addObject:withdrawCar];
        
        NSString *patente = @"";
        UIColor *color = [UIColor colorWithRed:150/255.0 green:150/255.0 blue:170/255.0 alpha:1];
        NSString *imageName = @"";

        NSMutableDictionary *dic = [[NSMutableDictionary alloc] initWithObjectsAndKeys:patente,@"patente",imageName,@"imagen",color,@"color", nil];
        [[vehicles objectAtIndex:currentCylinder] setObject:dic atIndexedSubscript:selectedIndex];
        [cylinderView reloadData];
    }
}

#pragma mark - UICollectionViewDataSource

- (NSInteger)collectionView:(UICollectionView *)collectionView numberOfItemsInSection:(NSInteger)section {
    return COLUMNS*LEVELS;
}

// The cell that is returned must be retrieved from a call to -dequeueReusableCellWithReuseIdentifier:forIndexPath:
- (UICollectionViewCell *)collectionView:(UICollectionView *)collectionView cellForItemAtIndexPath:(NSIndexPath *)indexPath {
    static NSString *identifier = @"PlatformCollectionViewCell";
    
    PlatformCollectionViewCell *cell = (PlatformCollectionViewCell *)[collectionView dequeueReusableCellWithReuseIdentifier:identifier forIndexPath:indexPath];
    
    NSMutableDictionary *dict = [[vehicles objectAtIndex:currentCylinder] objectAtIndex:indexPath.row];
    
    [cell.backgroundView setBackgroundColor:[dict objectForKey:@"color"]];
    [cell.vehicleIdLabel setText:[dict objectForKey:@"patente"]];
    [cell.vehicleImage setImage:[UIImage imageNamed:[dict objectForKey:@"imagen"]]];
    
    return cell;
}

#pragma mark -  UITableViewDataSource

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return [parkingSlot count];
}

// Row display. Implementers should *always* try to reuse cells by setting each cell's reuseIdentifier and querying for available reusable cells with dequeueReusableCellWithIdentifier:
// Cell gets various attributes set automatically based on table (separators) and data source (accessory views, editing controls)

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
    static NSString *identifier = @"SlotTableViewCell";
    
    SlotTableViewCell *cell = (SlotTableViewCell *)[tableView dequeueReusableCellWithIdentifier:identifier];
    
    NSMutableDictionary *dict = [parkingSlot objectAtIndex:indexPath.row];
    
    [cell.backgroundView setBackgroundColor:[dict objectForKey:@"color"]];
    [cell.vehicleIdLabel setText:[dict objectForKey:@"patente"]];
    [cell.vehicleImage setImage:[UIImage imageNamed:[dict objectForKey:@"imagen"]]];
    
    return cell;
}


@end
