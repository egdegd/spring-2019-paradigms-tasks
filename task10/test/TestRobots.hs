import Test.Tasty
import Test.Tasty.HUnit

import Robots

main :: IO ()
main = defaultMain testsRobots

testsRobots :: TestTree
testsRobots = let
        walter = robot "Walter" 50 50
        mike = robot "Mike" 30 100
        petr = robot "Peter" 40 80
        semen = robot "Semen" 5 500
    in testGroup "Unit tests for Robots task"
        [ testCase "Test for getName" $
            getName walter @?= "Walter"

        , testCase "Test for getAttack" $
            getAttack walter @?= 50

        , testCase "Test for getHealth" $
            getHealth walter @?= 50

        , testCase "Test for setName" $
            setName "NewName" mike @?= robot "NewName" 30 100

        , testCase "Test for setAttack" $
            setAttack 50 mike @?= robot "Mike" 50 100

        , testCase "Test for setHealth" $
            setHealth 90 mike @?= robot "Mike" 30 90

        , testCase "Test for printRobot" $
            printRobot walter @?= "Walter, attack: 50, health: 50"

        , testCase "Test for damage" $
            (getHealth $ damage mike 10) @?= 90

        , testCase "Test for isAlive" $
            isAlive walter @?= True

        , testCase "Test for fights" $
            (getHealth $ fight walter mike) @?= 50

        , testCase "Test for threeRoundFight" $
            threeRoundFight walter mike @?= robot "Walter" 50 20

        , testCase "Test for neueRobotAttak" $
            (getHealth $ neueRobotAttak mike) @?= 85

        , testCase "Test survivors" $
            survivors @?= [robot "First" 10 85, robot "Second" 20 35, robot "Third" 30 10]
        ]
