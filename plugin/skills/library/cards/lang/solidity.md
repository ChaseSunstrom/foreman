---
name: solidity
title: Solidity
area: lang
tags: [solidity, evm, foundry, hardhat, smart-contracts, security]
detect: [ext:.sol, file:foundry.toml, file:hardhat.config.*, dep:hardhat, dep:@openzeppelin/contracts]
related: [bash]
---
Solidity smart contracts: Foundry or Hardhat tests, OpenZeppelin building blocks, security-first patterns. Deployed code is hard to change.

## Verify
- `forge build`: compiles with the pinned compiler from `foundry.toml` (Hardhat: `npx hardhat compile`).
- `forge test -vvv`: runs `test/*.t.sol`, with traces on failure (Hardhat: `npx hardhat test`).
- `forge fmt --check`: formatting.
- `forge snapshot --check`: gas snapshot has not regressed.
- `slither .`: static analysis findings (reentrancy, unchecked calls, access control), when Slither is installed.

## Test first
Foundry tests are Solidity contracts inheriting `Test`; `testFail`-style is outdated, use `vm.expectRevert`.
```solidity
// test/Vault.t.sol
import {Test} from "forge-std/Test.sol";
import {Vault} from "../src/Vault.sol";

contract VaultTest is Test {
    Vault vault = new Vault();

    function test_RevertWhen_NonOwnerWithdraws() public {
        vm.prank(address(0xBAD));
        vm.expectRevert(Vault.NotOwner.selector);
        vault.withdraw(1 ether);
    }

    function testFuzz_DepositCredits(uint96 amount) public {
        vault.deposit{value: amount}();
        assertEq(vault.balanceOf(address(this)), amount);
    }
}
```

## Do
- Pin one `pragma solidity` version range (or exact) and set `solc` in config; use custom errors (`error NotOwner();`) over revert strings.
- Follow checks-effects-interactions: update state before external calls, and add OpenZeppelin `ReentrancyGuard` on value-moving functions.
- Use OpenZeppelin `Ownable2Step`/`AccessControl`, `SafeERC20` and audited ERC implementations instead of hand-rolled ones.
- Send ETH with `(bool ok, ) = to.call{value: v}(""); require(ok);` and handle the failure path.
- Mark visibility explicitly, use `immutable`/`constant` where possible, and emit events for every state change that matters.
- Fuzz and invariant test (`forge test` with `invariant_` functions) any accounting logic; fork-test integrations with `--fork-url`.
- For upgradeable contracts, use initializers (not constructors) and keep storage layout append-only.

## Avoid
- `tx.origin` for auth: phishable. Use `msg.sender`.
- `transfer`/`send` for ETH (fixed 2300 gas): breaks with contract wallets. Use `call` with a reentrancy guard.
- Unchecked return values of `call` and ERC20 `transfer`: silent failure. Check `ok` or use `SafeERC20`.
- `block.timestamp` or `blockhash` as randomness, and unbounded loops over user-controlled arrays: manipulable and DoS-prone. Use a commit-reveal or oracle, and paginate.
- `selfdestruct` and `delegatecall` to user-supplied addresses: removed semantics and storage takeover. Use fixed, audited targets.
- `unchecked { }` blocks to save gas without a proof: overflow. Keep default 0.8 checks unless proven safe.
- Reading price from a single spot AMM pool: flash-loan manipulation. Use a robust oracle with staleness checks.

## Review
- [ ] Every external or public state-changing function has explicit access control and the right modifier.
- [ ] State updates precede external calls, and return values of low-level calls are checked.
- [ ] Fuzz or invariant tests cover value-accounting and failure paths.
- [ ] Events, errors and NatSpec exist for all external functions.
- [ ] Storage layout and initializer safety are reviewed for upgradeable contracts.
